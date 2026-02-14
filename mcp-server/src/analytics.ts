/**
 * Analytics — non-blocking D1 event logging for MCP requests.
 *
 * Every function is wrapped in try/catch so a DB failure
 * never breaks an MCP response.
 */

export interface AnalyticsEvent {
  method: string;
  toolName: string | null;
  params: string | null;
  resultSize: number | null;
  isError: boolean;
  errorMsg: string | null;
  durationMs: number;
  userAgent: string | null;
  cfCountry: string | null;
}

/** Extract only the small, useful bits from tool arguments. */
export function sanitizeParams(
  method: string,
  params: Record<string, unknown> | undefined
): string | null {
  if (!params) return null;

  if (method === "tools/call") {
    const args = params.arguments;
    if (!args || typeof args !== "object" || Array.isArray(args)) return null;
    // Keep only short string values (query, path, section, slug, etc.)
    const safe: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(args as Record<string, unknown>)) {
      if (typeof v === "string" && v.length <= 200) {
        safe[k] = v;
      } else if (typeof v === "number" || typeof v === "boolean") {
        safe[k] = v;
      }
    }
    return Object.keys(safe).length > 0 ? JSON.stringify(safe) : null;
  }

  if (method === "resources/read" && typeof params.uri === "string") {
    return JSON.stringify({ uri: params.uri });
  }

  return null;
}

/** Character count of the JSON-RPC result text content. */
export function getResultSize(responseBody: unknown): number | null {
  try {
    const body = responseBody as { result?: unknown };
    if (!body?.result) return null;
    return JSON.stringify(body.result).length;
  } catch (err) {
    console.error("[analytics] Failed to compute result size:", err);
    return null;
  }
}

/** INSERT one row into mcp_events. Never throws. */
export async function logEvent(
  db: D1Database,
  event: AnalyticsEvent
): Promise<void> {
  try {
    await db
      .prepare(
        `INSERT INTO mcp_events
           (method, tool_name, params, result_size, is_error, error_msg, duration_ms, user_agent, cf_country)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`
      )
      .bind(
        event.method,
        event.toolName,
        event.params,
        event.resultSize,
        event.isError ? 1 : 0,
        event.errorMsg,
        event.durationMs,
        event.userAgent,
        event.cfCountry
      )
      .run();
  } catch (err) {
    console.error(JSON.stringify({
      level: "error",
      component: "analytics",
      operation: "logEvent",
      method: event.method,
      toolName: event.toolName,
      error: err instanceof Error ? err.message : String(err),
    }));
  }
}
