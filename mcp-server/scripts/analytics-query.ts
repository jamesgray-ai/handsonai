#!/usr/bin/env tsx
/**
 * CLI for querying MCP analytics via the Cloudflare D1 REST API.
 *
 * Usage:  npx tsx scripts/analytics-query.ts <command> [options]
 *
 * Requires env vars: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_D1_DATABASE_ID
 */

const COMMANDS: Record<string, string> = {
  "top-queries":  "Most frequent search queries",
  "tool-usage":   "Tool call breakdown",
  "daily-volume": "Events per day",
  "top-pages":    "Most requested pages (get_page)",
  "errors":       "Error rate by day",
  "zero-results": "Searches that returned no results",
  "clients":      "User-agent breakdown",
  "raw-sql":      "Run arbitrary SQL",
};

function env(key: string): string {
  const val = process.env[key];
  if (!val) {
    console.error(`Missing env var: ${key}`);
    process.exit(1);
  }
  return val;
}

function parseDays(args: string[]): number {
  const flag = args.find((a) => a.startsWith("--days="));
  if (!flag) return 30;
  const value = parseInt(flag.split("=")[1], 10);
  if (isNaN(value) || value <= 0) {
    console.error(`Invalid --days value: "${flag.split("=")[1]}". Must be a positive integer.`);
    process.exit(1);
  }
  return value;
}

async function queryD1(sql: string, params: unknown[] = []): Promise<unknown[]> {
  const accountId = env("CLOUDFLARE_ACCOUNT_ID");
  const dbId = env("CLOUDFLARE_D1_DATABASE_ID");
  const token = env("CLOUDFLARE_API_TOKEN");

  const res = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${accountId}/d1/database/${dbId}/query`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sql, params }),
    }
  );

  if (!res.ok) {
    const text = await res.text();
    console.error(`Cloudflare API error (${res.status}):`, text);
    process.exit(1);
  }

  const data = (await res.json()) as {
    result: { results: unknown[] }[];
    success: boolean;
    errors: unknown[];
  };

  if (!data.success) {
    console.error("D1 query failed:", JSON.stringify(data.errors, null, 2));
    process.exit(1);
  }

  if (!Array.isArray(data.result) || data.result.length === 0 || !data.result[0].results) {
    console.error("Unexpected D1 API response shape:", JSON.stringify(data, null, 2));
    process.exit(1);
  }

  return data.result[0].results;
}

function printTable(rows: unknown[]) {
  if (rows.length === 0) {
    console.log("(no results)");
    return;
  }
  console.table(rows);
}

const QUERIES: Record<string, (args: string[]) => Promise<void>> = {
  "top-queries": async (args) => {
    const days = parseDays(args);
    const rows = await queryD1(
      `SELECT json_extract(params, '$.query') AS query, COUNT(*) AS count
       FROM mcp_events
       WHERE tool_name = 'search_cookbook'
         AND params IS NOT NULL
         AND timestamp >= datetime('now', ?)
       GROUP BY query
       ORDER BY count DESC
       LIMIT 25`,
      [`-${days} days`]
    );
    console.log(`\nTop search queries (last ${days} days):\n`);
    printTable(rows);
  },

  "tool-usage": async (args) => {
    const days = parseDays(args);
    const rows = await queryD1(
      `SELECT tool_name, COUNT(*) AS count,
              ROUND(AVG(duration_ms), 1) AS avg_ms,
              SUM(is_error) AS errors
       FROM mcp_events
       WHERE method = 'tools/call'
         AND timestamp >= datetime('now', ?)
       GROUP BY tool_name
       ORDER BY count DESC`,
      [`-${days} days`]
    );
    console.log(`\nTool usage (last ${days} days):\n`);
    printTable(rows);
  },

  "daily-volume": async (args) => {
    const days = parseDays(args);
    const rows = await queryD1(
      `SELECT date(timestamp) AS day, COUNT(*) AS events,
              SUM(CASE WHEN method = 'tools/call' THEN 1 ELSE 0 END) AS tool_calls
       FROM mcp_events
       WHERE timestamp >= datetime('now', ?)
       GROUP BY day
       ORDER BY day DESC`,
      [`-${days} days`]
    );
    console.log(`\nDaily volume (last ${days} days):\n`);
    printTable(rows);
  },

  "top-pages": async (args) => {
    const days = parseDays(args);
    const rows = await queryD1(
      `SELECT json_extract(params, '$.path') AS page, COUNT(*) AS count
       FROM mcp_events
       WHERE tool_name = 'get_page'
         AND params IS NOT NULL
         AND timestamp >= datetime('now', ?)
       GROUP BY page
       ORDER BY count DESC
       LIMIT 25`,
      [`-${days} days`]
    );
    console.log(`\nTop pages (last ${days} days):\n`);
    printTable(rows);
  },

  errors: async (args) => {
    const days = parseDays(args);
    const rows = await queryD1(
      `SELECT date(timestamp) AS day,
              COUNT(*) AS total,
              SUM(is_error) AS errors,
              ROUND(100.0 * SUM(is_error) / COUNT(*), 1) AS error_pct
       FROM mcp_events
       WHERE timestamp >= datetime('now', ?)
       GROUP BY day
       ORDER BY day DESC`,
      [`-${days} days`]
    );
    console.log(`\nError rate by day (last ${days} days):\n`);
    printTable(rows);
  },

  "zero-results": async (args) => {
    const days = parseDays(args);
    const rows = await queryD1(
      `SELECT json_extract(params, '$.query') AS query, COUNT(*) AS count
       FROM mcp_events
       WHERE tool_name = 'search_cookbook'
         AND params IS NOT NULL
         AND result_size IS NOT NULL
         AND result_size < 100
         AND timestamp >= datetime('now', ?)
       GROUP BY query
       ORDER BY count DESC
       LIMIT 25`,
      [`-${days} days`]
    );
    console.log(`\nZero/low-result searches — content gaps (last ${days} days):\n`);
    printTable(rows);
  },

  clients: async (args) => {
    const days = parseDays(args);
    const rows = await queryD1(
      `SELECT user_agent, COUNT(*) AS count
       FROM mcp_events
       WHERE timestamp >= datetime('now', ?)
       GROUP BY user_agent
       ORDER BY count DESC
       LIMIT 20`,
      [`-${days} days`]
    );
    console.log(`\nClients (last ${days} days):\n`);
    printTable(rows);
  },

  "raw-sql": async (args) => {
    const sql = args.find((a) => !a.startsWith("--"));
    if (!sql) {
      console.error("Usage: raw-sql <query>");
      process.exit(1);
    }
    if (!/^\s*SELECT\b/i.test(sql)) {
      console.error("raw-sql only supports SELECT queries. Use `wrangler d1 execute` for mutations.");
      process.exit(1);
    }
    const rows = await queryD1(sql);
    printTable(rows);
  },
};

// --- main ---
const [command, ...rest] = process.argv.slice(2);

if (!command || !COMMANDS[command]) {
  console.log("Usage: npx tsx scripts/analytics-query.ts <command> [options]\n");
  console.log("Commands:");
  for (const [cmd, desc] of Object.entries(COMMANDS)) {
    console.log(`  ${cmd.padEnd(16)} ${desc}`);
  }
  console.log("\nOptions:");
  console.log("  --days=N       Look-back window (default: 30)");
  process.exit(0);
}

QUERIES[command](rest).catch((err) => {
  console.error("Command failed:", err instanceof Error ? err.message : err);
  process.exit(1);
});
