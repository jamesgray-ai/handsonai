/**
 * Hands-on AI Cookbook — MCP Analytics Dashboard — API handlers + HTML UI.
 *
 * All dashboard logic lives in this single file:
 * - Cookie-based authentication
 * - 7 analytics query endpoints
 * - Dashboard HTML with Chart.js visualizations
 */

import type { Env } from "./types.js";

const COOKIE_NAME = "analytics_session";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 30; // 30 days

// ---------------------------------------------------------------------------
// Authentication
// ---------------------------------------------------------------------------

/** Constant-time string comparison using HMAC to prevent timing attacks. */
async function timingSafeEqual(a: string, b: string): Promise<boolean> {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(a),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, encoder.encode(b));
  const expected = await crypto.subtle.sign("HMAC", key, encoder.encode(a));
  const sigBytes = new Uint8Array(sig);
  const expectedBytes = new Uint8Array(expected);
  if (sigBytes.length !== expectedBytes.length) return false;
  let diff = 0;
  for (let i = 0; i < sigBytes.length; i++) {
    diff |= sigBytes[i] ^ expectedBytes[i];
  }
  return diff === 0;
}

/** Check cookie or ?token= query param. Returns null if authenticated, or a Response (401 / redirect). */
export async function authenticateDashboard(
  request: Request,
  url: URL,
  env: Env
): Promise<Response | null> {
  const token = url.searchParams.get("token");

  // Token in query param — validate, set cookie, redirect to clean URL
  if (token) {
    if (!(await timingSafeEqual(token, env.ANALYTICS_TOKEN))) {
      return new Response("Unauthorized", { status: 401 });
    }
    const cleanUrl = new URL(url);
    cleanUrl.searchParams.delete("token");
    return new Response(null, {
      status: 302,
      headers: {
        Location: cleanUrl.pathname,
        "Set-Cookie": `${COOKIE_NAME}=${token}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${COOKIE_MAX_AGE}`,
      },
    });
  }

  // Check cookie
  const cookies = request.headers.get("Cookie") || "";
  const match = cookies.match(new RegExp(`${COOKIE_NAME}=([^;]+)`));
  if (match && (await timingSafeEqual(match[1], env.ANALYTICS_TOKEN))) {
    return null; // authenticated
  }

  return new Response("Unauthorized", { status: 401 });
}

// ---------------------------------------------------------------------------
// Analytics API
// ---------------------------------------------------------------------------

type QueryResult = Record<string, unknown>[];

async function queryD1(db: D1Database, sql: string, params: unknown[] = []): Promise<QueryResult> {
  const stmt = db.prepare(sql);
  const bound = params.length > 0 ? stmt.bind(...params) : stmt;
  const result = await bound.all();
  return result.results as QueryResult;
}

const QUERIES: Record<string, (db: D1Database, days: number) => Promise<QueryResult>> = {
  "top-queries": (db, days) =>
    queryD1(
      db,
      `SELECT json_extract(params, '$.query') AS query, COUNT(*) AS count
       FROM mcp_events
       WHERE tool_name = 'search_cookbook'
         AND params IS NOT NULL
         AND timestamp >= datetime('now', ?)
       GROUP BY query
       ORDER BY count DESC
       LIMIT 25`,
      [`-${days} days`]
    ),

  "tool-usage": (db, days) =>
    queryD1(
      db,
      `SELECT tool_name, COUNT(*) AS count,
              ROUND(AVG(duration_ms), 1) AS avg_ms,
              SUM(is_error) AS errors
       FROM mcp_events
       WHERE method = 'tools/call'
         AND timestamp >= datetime('now', ?)
       GROUP BY tool_name
       ORDER BY count DESC`,
      [`-${days} days`]
    ),

  "daily-volume": (db, days) =>
    queryD1(
      db,
      `SELECT date(timestamp) AS day, COUNT(*) AS events,
              SUM(CASE WHEN method = 'tools/call' THEN 1 ELSE 0 END) AS tool_calls
       FROM mcp_events
       WHERE timestamp >= datetime('now', ?)
       GROUP BY day
       ORDER BY day ASC`,
      [`-${days} days`]
    ),

  "top-pages": (db, days) =>
    queryD1(
      db,
      `SELECT json_extract(params, '$.path') AS page, COUNT(*) AS count
       FROM mcp_events
       WHERE tool_name = 'get_page'
         AND params IS NOT NULL
         AND timestamp >= datetime('now', ?)
       GROUP BY page
       ORDER BY count DESC
       LIMIT 25`,
      [`-${days} days`]
    ),

  errors: (db, days) =>
    queryD1(
      db,
      `SELECT date(timestamp) AS day,
              COUNT(*) AS total,
              SUM(is_error) AS errors,
              ROUND(100.0 * SUM(is_error) / COUNT(*), 1) AS error_pct
       FROM mcp_events
       WHERE timestamp >= datetime('now', ?)
       GROUP BY day
       ORDER BY day ASC`,
      [`-${days} days`]
    ),

  "zero-results": (db, days) =>
    queryD1(
      db,
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
    ),

  clients: (db, days) =>
    queryD1(
      db,
      `SELECT user_agent, COUNT(*) AS count
       FROM mcp_events
       WHERE timestamp >= datetime('now', ?)
       GROUP BY user_agent
       ORDER BY count DESC
       LIMIT 20`,
      [`-${days} days`]
    ),

  geography: (db, days) =>
    queryD1(
      db,
      `SELECT cf_country AS country, COUNT(*) AS count
       FROM mcp_events
       WHERE cf_country IS NOT NULL
         AND timestamp >= datetime('now', ?)
       GROUP BY cf_country
       ORDER BY count DESC
       LIMIT 25`,
      [`-${days} days`]
    ),

  "section-filters": (db, days) =>
    queryD1(
      db,
      `SELECT json_extract(params, '$.section') AS section, COUNT(*) AS count
       FROM mcp_events
       WHERE tool_name = 'search_cookbook'
         AND params IS NOT NULL
         AND json_extract(params, '$.section') IS NOT NULL
         AND timestamp >= datetime('now', ?)
       GROUP BY section
       ORDER BY count DESC`,
      [`-${days} days`]
    ),

  "building-blocks": (db, days) =>
    queryD1(
      db,
      `SELECT json_extract(params, '$.name') AS block, COUNT(*) AS count
       FROM mcp_events
       WHERE tool_name = 'get_building_block'
         AND params IS NOT NULL
         AND timestamp >= datetime('now', ?)
       GROUP BY block
       ORDER BY count DESC`,
      [`-${days} days`]
    ),

  "setup-guides": (db, days) =>
    queryD1(
      db,
      `SELECT json_extract(params, '$.tool') AS tool, COUNT(*) AS count
       FROM mcp_events
       WHERE tool_name = 'get_setup_guide'
         AND params IS NOT NULL
         AND timestamp >= datetime('now', ?)
       GROUP BY tool
       ORDER BY count DESC`,
      [`-${days} days`]
    ),
};

export async function handleAnalyticsAPI(url: URL, env: Env): Promise<Response> {
  const endpoint = url.pathname.replace("/api/analytics/", "");
  const queryFn = QUERIES[endpoint];

  if (!queryFn) {
    return new Response(JSON.stringify({ error: "Unknown endpoint" }), {
      status: 404,
      headers: { "Content-Type": "application/json" },
    });
  }

  const days = Math.min(Math.max(parseInt(url.searchParams.get("days") || "30", 10) || 30, 1), 365);

  try {
    const results = await queryFn(env.DB, days);
    return new Response(JSON.stringify({ results, days }), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    console.error(`[dashboard] Query error (${endpoint}):`, err);
    return new Response(JSON.stringify({ error: "Query failed" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}

// ---------------------------------------------------------------------------
// Dashboard HTML
// ---------------------------------------------------------------------------

export function getDashboardHTML(): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hands-on AI Cookbook — MCP Analytics Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
  <style>
    :root {
      --bg: #0f1117;
      --surface: #1a1d27;
      --border: #2a2d3a;
      --text: #e1e4ed;
      --text-muted: #8b8fa3;
      --accent: #6366f1;
      --accent-light: #818cf8;
      --green: #22c55e;
      --red: #ef4444;
      --orange: #f59e0b;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }
    header {
      padding: 1.5rem 2rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }
    header h1 { font-size: 1.25rem; font-weight: 600; }
    .controls { display: flex; gap: 0.5rem; align-items: center; }
    .time-btn {
      padding: 0.4rem 0.8rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.85rem;
      transition: all 0.15s;
    }
    .time-btn:hover { border-color: var(--accent); color: var(--text); }
    .time-btn.active { background: var(--accent); color: white; border-color: var(--accent); }
    .refresh-btn {
      padding: 0.4rem 0.8rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.85rem;
      margin-left: 0.5rem;
    }
    .refresh-btn:hover { border-color: var(--accent); color: var(--text); }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 500px), 1fr));
      gap: 1.25rem;
      padding: 1.5rem 2rem;
    }
    .panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
      min-height: 280px;
    }
    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    .panel-title { font-size: 0.95rem; font-weight: 600; }
    .panel-updated { font-size: 0.75rem; color: var(--text-muted); }
    .panel-body { position: relative; }
    .panel canvas { max-height: 220px; }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
    }
    th {
      text-align: left;
      padding: 0.5rem 0.75rem;
      border-bottom: 1px solid var(--border);
      color: var(--text-muted);
      font-weight: 500;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    td {
      padding: 0.45rem 0.75rem;
      border-bottom: 1px solid var(--border);
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(99, 102, 241, 0.05); }
    .highlight td { background: rgba(239, 68, 68, 0.08); }
    .num { text-align: right; font-variant-numeric: tabular-nums; }
    .loading {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 200px;
      color: var(--text-muted);
    }
    .error-msg { color: var(--red); text-align: center; padding: 2rem; }
    .table-scroll { max-height: 320px; overflow-y: auto; }
    @media (max-width: 640px) {
      header { padding: 1rem; }
      .grid { padding: 1rem; gap: 1rem; }
      .panel { padding: 1rem; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Hands-on AI Cookbook — MCP Analytics</h1>
    <div class="controls">
      <button class="time-btn" data-days="7">7d</button>
      <button class="time-btn active" data-days="30">30d</button>
      <button class="time-btn" data-days="90">90d</button>
      <button class="refresh-btn" id="refreshBtn">Refresh</button>
    </div>
  </header>
  <div class="grid">
    <div class="panel" id="p-daily-volume">
      <div class="panel-header">
        <span class="panel-title">Daily Volume</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-tool-usage">
      <div class="panel-header">
        <span class="panel-title">Tool Usage</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-top-queries">
      <div class="panel-header">
        <span class="panel-title">Top Search Queries</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-top-pages">
      <div class="panel-header">
        <span class="panel-title">Top Pages</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-zero-results">
      <div class="panel-header">
        <span class="panel-title">Content Gaps (Zero Results)</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-errors">
      <div class="panel-header">
        <span class="panel-title">Error Rate</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-clients">
      <div class="panel-header">
        <span class="panel-title">Clients</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-geography">
      <div class="panel-header">
        <span class="panel-title">Geography</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-section-filters">
      <div class="panel-header">
        <span class="panel-title">Section Filter Usage</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-building-blocks">
      <div class="panel-header">
        <span class="panel-title">Building Block Popularity</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
    <div class="panel" id="p-setup-guides">
      <div class="panel-header">
        <span class="panel-title">Setup Guide Demand</span>
        <span class="panel-updated" data-updated></span>
      </div>
      <div class="panel-body"><div class="loading">Loading...</div></div>
    </div>
  </div>
  <script>
    let currentDays = 30;
    const charts = {};

    document.querySelectorAll('.time-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        document.querySelectorAll('.time-btn').forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
        currentDays = parseInt(btn.dataset.days);
        loadAll();
      });
    });

    document.getElementById('refreshBtn').addEventListener('click', loadAll);

    async function fetchData(endpoint) {
      const res = await fetch('/api/analytics/' + endpoint + '?days=' + currentDays);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return (await res.json()).results;
    }

    function setUpdated(panelId) {
      const el = document.querySelector('#' + panelId + ' [data-updated]');
      if (el) el.textContent = 'Updated ' + new Date().toLocaleTimeString();
    }

    function clearPanel(panelId) {
      const body = document.querySelector('#' + panelId + ' .panel-body');
      while (body.firstChild) body.removeChild(body.firstChild);
      return body;
    }

    function showError(panelId, msg) {
      const body = clearPanel(panelId);
      const div = document.createElement('div');
      div.className = 'error-msg';
      div.textContent = msg;
      body.appendChild(div);
    }

    function showNoData(panelId) {
      const body = clearPanel(panelId);
      const div = document.createElement('div');
      div.className = 'loading';
      div.textContent = 'No data';
      body.appendChild(div);
    }

    function buildTable(headers, rows, container) {
      if (!rows.length) {
        const div = document.createElement('div');
        div.className = 'loading';
        div.textContent = 'No data';
        container.appendChild(div);
        return;
      }
      const wrapper = document.createElement('div');
      wrapper.className = 'table-scroll';
      const table = document.createElement('table');
      const thead = document.createElement('thead');
      const headRow = document.createElement('tr');
      headers.forEach(function(h) {
        const th = document.createElement('th');
        th.textContent = h.label;
        if (h.num) th.className = 'num';
        headRow.appendChild(th);
      });
      thead.appendChild(headRow);
      table.appendChild(thead);
      const tbody = document.createElement('tbody');
      rows.forEach(function(row) {
        const tr = document.createElement('tr');
        if (row._highlight) tr.className = 'highlight';
        headers.forEach(function(h) {
          const td = document.createElement('td');
          td.textContent = String(row[h.key] ?? '');
          if (h.num) td.className = 'num';
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      wrapper.appendChild(table);
      container.appendChild(wrapper);
    }

    function destroyChart(id) {
      if (charts[id]) { charts[id].destroy(); delete charts[id]; }
    }

    function createCanvas(container, maxHeight) {
      const canvas = document.createElement('canvas');
      if (maxHeight) canvas.style.maxHeight = maxHeight;
      container.appendChild(canvas);
      return canvas.getContext('2d');
    }

    // --- Panel renderers ---

    async function loadDailyVolume() {
      const id = 'p-daily-volume';
      try {
        const data = await fetchData('daily-volume');
        const body = clearPanel(id);
        destroyChart(id);
        const ctx = createCanvas(body);
        charts[id] = new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.map(function(d) { return d.day; }),
            datasets: [
              { label: 'All Events', data: data.map(function(d) { return d.events; }), borderColor: '#6366f1', backgroundColor: 'rgba(99,102,241,0.1)', fill: true, tension: 0.3 },
              { label: 'Tool Calls', data: data.map(function(d) { return d.tool_calls; }), borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.1)', fill: true, tension: 0.3 },
            ],
          },
          options: { responsive: true, maintainAspectRatio: false, scales: { x: { ticks: { color: '#8b8fa3', maxTicksLimit: 10 }, grid: { color: '#2a2d3a' } }, y: { ticks: { color: '#8b8fa3' }, grid: { color: '#2a2d3a' } } }, plugins: { legend: { labels: { color: '#e1e4ed' } } } },
        });
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadToolUsage() {
      const id = 'p-tool-usage';
      try {
        const data = await fetchData('tool-usage');
        const body = clearPanel(id);
        destroyChart(id);
        var ctx = createCanvas(body, '160px');
        charts[id] = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.map(function(d) { return d.tool_name; }),
            datasets: [{ label: 'Calls', data: data.map(function(d) { return d.count; }), backgroundColor: '#6366f1' }],
          },
          options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y', scales: { x: { ticks: { color: '#8b8fa3' }, grid: { color: '#2a2d3a' } }, y: { ticks: { color: '#8b8fa3' }, grid: { display: false } } }, plugins: { legend: { display: false } } },
        });
        buildTable(
          [{ label: 'Tool', key: 'tool_name' }, { label: 'Calls', key: 'count', num: true }, { label: 'Avg ms', key: 'avg_ms', num: true }, { label: 'Errors', key: 'errors', num: true }],
          data, body
        );
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadTopQueries() {
      const id = 'p-top-queries';
      try {
        const data = await fetchData('top-queries');
        const body = clearPanel(id);
        buildTable(
          [{ label: 'Query', key: 'query' }, { label: 'Count', key: 'count', num: true }],
          data, body
        );
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadTopPages() {
      const id = 'p-top-pages';
      try {
        const data = await fetchData('top-pages');
        const body = clearPanel(id);
        buildTable(
          [{ label: 'Page', key: 'page' }, { label: 'Count', key: 'count', num: true }],
          data, body
        );
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadZeroResults() {
      const id = 'p-zero-results';
      try {
        const data = await fetchData('zero-results');
        data.forEach(function(d) { d._highlight = true; });
        const body = clearPanel(id);
        buildTable(
          [{ label: 'Query', key: 'query' }, { label: 'Count', key: 'count', num: true }],
          data, body
        );
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadErrors() {
      const id = 'p-errors';
      try {
        const data = await fetchData('errors');
        const body = clearPanel(id);
        destroyChart(id);
        const ctx = createCanvas(body);
        charts[id] = new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.map(function(d) { return d.day; }),
            datasets: [{ label: 'Error %', data: data.map(function(d) { return d.error_pct; }), borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.1)', fill: true, tension: 0.3 }],
          },
          options: { responsive: true, maintainAspectRatio: false, scales: { x: { ticks: { color: '#8b8fa3', maxTicksLimit: 10 }, grid: { color: '#2a2d3a' } }, y: { ticks: { color: '#8b8fa3', callback: function(v) { return v + '%'; } }, grid: { color: '#2a2d3a' } } }, plugins: { legend: { labels: { color: '#e1e4ed' } } } },
        });
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadClients() {
      const id = 'p-clients';
      try {
        const data = await fetchData('clients');
        const body = clearPanel(id);
        destroyChart(id);
        const colors = ['#6366f1','#22c55e','#f59e0b','#ef4444','#06b6d4','#ec4899','#8b5cf6','#14b8a6','#f97316','#64748b'];
        const ctx = createCanvas(body);
        charts[id] = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: data.map(function(d) { return String(d.user_agent || 'Unknown').substring(0, 40); }),
            datasets: [{ data: data.map(function(d) { return d.count; }), backgroundColor: colors.slice(0, data.length) }],
          },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { color: '#e1e4ed', font: { size: 11 }, boxWidth: 12 } } } },
        });
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadGeography() {
      const id = 'p-geography';
      try {
        const data = await fetchData('geography');
        const body = clearPanel(id);
        buildTable(
          [{ label: 'Country', key: 'country' }, { label: 'Requests', key: 'count', num: true }],
          data, body
        );
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadSectionFilters() {
      const id = 'p-section-filters';
      try {
        const data = await fetchData('section-filters');
        const body = clearPanel(id);
        buildTable(
          [{ label: 'Section', key: 'section' }, { label: 'Searches', key: 'count', num: true }],
          data, body
        );
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadBuildingBlocks() {
      const id = 'p-building-blocks';
      try {
        const data = await fetchData('building-blocks');
        const body = clearPanel(id);
        buildTable(
          [{ label: 'Building Block', key: 'block' }, { label: 'Lookups', key: 'count', num: true }],
          data, body
        );
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    async function loadSetupGuides() {
      const id = 'p-setup-guides';
      try {
        const data = await fetchData('setup-guides');
        const body = clearPanel(id);
        buildTable(
          [{ label: 'Tool', key: 'tool' }, { label: 'Lookups', key: 'count', num: true }],
          data, body
        );
        setUpdated(id);
      } catch (e) { showError(id, 'Failed to load'); }
    }

    function loadAll() {
      loadDailyVolume();
      loadToolUsage();
      loadTopQueries();
      loadTopPages();
      loadZeroResults();
      loadErrors();
      loadClients();
      loadGeography();
      loadSectionFilters();
      loadBuildingBlocks();
      loadSetupGuides();
    }

    loadAll();
  </script>
</body>
</html>`;
}
