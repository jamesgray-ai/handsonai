/**
 * Hands-on AI Cookbook MCP Server — Cloudflare Worker
 *
 * Implements the MCP protocol over Streamable HTTP (stateless JSON mode).
 * Serves cookbook content via 7 tools and 1 resource.
 */

import type { ContentIndex, Env, JsonRpcRequest, JsonRpcResponse } from "./types.js";
import {
  TOOL_DEFINITIONS,
  RESOURCE_DEFINITION,
  handleToolCall,
  handleResourceRead,
} from "./tools.js";
import { logEvent, sanitizeParams, getResultSize } from "./analytics.js";
import contentIndex from "../content-index.json";

const index = contentIndex as ContentIndex;

const PROTOCOL_VERSION = "2025-03-26";
const SERVER_INFO = {
  name: "handsonai-mcp-server",
  version: "1.0.0",
};

const MAX_BODY_SIZE = 1_000_000; // 1 MB

// Public read-only API — wildcard CORS is intentional.
// If authentication is added in the future, restrict to specific origins.
const CORS_HEADERS: Record<string, string> = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, GET, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Mcp-Session-Id",
};

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...CORS_HEADERS },
  });
}

function rpcResult(id: number | string, result: unknown): Response {
  const response: JsonRpcResponse = { jsonrpc: "2.0", id, result };
  return jsonResponse(response);
}

function rpcError(
  id: number | string | null,
  code: number,
  message: string
): Response {
  const response: JsonRpcResponse = {
    jsonrpc: "2.0",
    id: id ?? 0,
    error: { code, message },
  };
  return jsonResponse(response);
}

function handleMethod(
  method: string,
  params: Record<string, unknown> | undefined,
  id: number | string
): Response {
  switch (method) {
    case "initialize":
      return rpcResult(id, {
        protocolVersion: PROTOCOL_VERSION,
        capabilities: {
          tools: { listChanged: false },
          resources: { subscribe: false, listChanged: false },
        },
        serverInfo: SERVER_INFO,
      });

    case "ping":
      return rpcResult(id, {});

    case "tools/list":
      return rpcResult(id, { tools: TOOL_DEFINITIONS });

    case "tools/call": {
      const toolName = params?.name;
      const toolArgs = (params?.arguments ?? {}) as Record<string, unknown>;
      if (typeof toolName !== "string" || !toolName) {
        return rpcError(id, -32602, "Missing or invalid tool name in params.name");
      }
      try {
        const result = handleToolCall(toolName, toolArgs, index);
        return rpcResult(id, result);
      } catch (err) {
        console.error("[mcp-server] Tool call error:", err);
        return rpcResult(id, {
          content: [{ type: "text", text: "An error occurred processing your request." }],
          isError: true,
        });
      }
    }

    case "resources/list":
      return rpcResult(id, { resources: [RESOURCE_DEFINITION] });

    case "resources/read": {
      const uri = params?.uri;
      if (typeof uri !== "string" || !uri) {
        return rpcError(id, -32602, "Missing or invalid resource URI in params.uri");
      }
      try {
        const result = handleResourceRead(uri, index);
        return rpcResult(id, result);
      } catch (err) {
        console.error("[mcp-server] Resource read error:", err);
        return rpcError(id, -32602, "Resource not found");
      }
    }

    default:
      return rpcError(id, -32601, `Method not found: ${method}`);
  }
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    try {
      const url = new URL(request.url);

      // CORS preflight
      if (request.method === "OPTIONS") {
        return new Response(null, { status: 204, headers: CORS_HEADERS });
      }

      // Health check
      if (url.pathname === "/" || url.pathname === "/health") {
        return jsonResponse({
          status: "ok",
          server: SERVER_INFO.name,
          version: SERVER_INFO.version,
          pages: index.pageCount,
        });
      }

      // MCP endpoint
      if (url.pathname === "/mcp") {
        // Session cleanup — stateless server, just acknowledge
        if (request.method === "DELETE") {
          return new Response(null, { status: 200, headers: CORS_HEADERS });
        }

        if (request.method !== "POST") {
          return new Response("Method not allowed. Use POST.", {
            status: 405,
            headers: CORS_HEADERS,
          });
        }

        // Request body size limit
        const contentLength = request.headers.get("content-length");
        if (contentLength && parseInt(contentLength) > MAX_BODY_SIZE) {
          return rpcError(null, -32700, "Request body too large");
        }

        let body: JsonRpcRequest;
        try {
          body = (await request.json()) as JsonRpcRequest;
        } catch {
          return rpcError(null, -32700, "Parse error: invalid JSON");
        }

        if (body.jsonrpc !== "2.0") {
          return rpcError(
            body.id ?? null,
            -32600,
            "Invalid request: must be JSON-RPC 2.0"
          );
        }

        // Notifications have no id — acknowledge with 202
        if (body.id === undefined || body.id === null) {
          return new Response(null, { status: 202, headers: CORS_HEADERS });
        }

        const start = Date.now();
        const response = handleMethod(body.method, body.params, body.id);
        const durationMs = Date.now() - start;

        // Only log tools/call and resources/read — skip protocol handshake noise
        if (body.method === "tools/call" || body.method === "resources/read") {
          const toolName =
            body.method === "tools/call" && typeof body.params?.name === "string"
              ? body.params.name
              : null;

          const responseClone = response.clone();
          ctx.waitUntil(
            (async () => {
              let responseBody: unknown;
              try {
                responseBody = await responseClone.json();
              } catch (err) {
                console.error("[analytics] Failed to parse response JSON:", err);
                return;
              }

              const rpcBody = responseBody as { error?: unknown; result?: { isError?: boolean } };
              const isError = !!(rpcBody.error || rpcBody.result?.isError);
              const errorMsg = rpcBody.error
                ? JSON.stringify(rpcBody.error)
                : null;

              await logEvent(env.DB, {
                method: body.method,
                toolName,
                params: sanitizeParams(body.method, body.params),
                resultSize: getResultSize(responseBody),
                isError,
                errorMsg,
                durationMs,
                userAgent: request.headers.get("user-agent"),
                cfCountry: (request as unknown as { cf?: { country?: string } }).cf?.country ?? null,
              });
            })()
          );
        }

        return response;
      }

      return new Response("Not found", { status: 404, headers: CORS_HEADERS });
    } catch (err) {
      console.error("[mcp-server] Unhandled error:", err);
      return new Response(
        JSON.stringify({
          jsonrpc: "2.0",
          id: 0,
          error: { code: -32603, message: "Internal server error" },
        }),
        {
          status: 500,
          headers: { "Content-Type": "application/json", ...CORS_HEADERS },
        }
      );
    }
  },
};
