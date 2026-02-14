CREATE TABLE IF NOT EXISTS mcp_events (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp   TEXT    NOT NULL DEFAULT (datetime('now')),
  method      TEXT    NOT NULL,
  tool_name   TEXT,
  params      TEXT,
  result_size INTEGER,
  is_error    INTEGER NOT NULL DEFAULT 0,
  error_msg   TEXT,
  duration_ms REAL,
  user_agent  TEXT,
  cf_country  TEXT
);

CREATE INDEX idx_events_timestamp ON mcp_events(timestamp);
CREATE INDEX idx_events_method ON mcp_events(method);
CREATE INDEX idx_events_tool_name ON mcp_events(tool_name);
CREATE INDEX idx_events_tool_timestamp ON mcp_events(tool_name, timestamp);
