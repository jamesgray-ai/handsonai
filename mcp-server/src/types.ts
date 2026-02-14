export interface Env {
  DB: D1Database;
}

export interface Page {
  path: string;
  title: string;
  description: string;
  section: string;
  content: string;
  url: string;
  question?: string;
  short_answer?: string;
}

export interface ContentIndex {
  generatedAt: string;
  pageCount: number;
  pages: Page[];
  sections: Record<string, { label: string; count: number }>;
}

export interface JsonRpcRequest {
  jsonrpc: "2.0";
  id?: number | string;
  method: string;
  params?: Record<string, unknown>;
}

export interface JsonRpcResponse {
  jsonrpc: "2.0";
  id: number | string;
  result?: unknown;
  error?: { code: number; message: string; data?: unknown };
}

export interface McpToolDefinition {
  name: string;
  description: string;
  inputSchema: {
    type: "object";
    properties: Record<string, unknown>;
    required?: string[];
  };
  annotations?: Record<string, boolean>;
}

export interface McpResourceDefinition {
  uri: string;
  name: string;
  description: string;
  mimeType: string;
}
