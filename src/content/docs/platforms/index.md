---
title: Platforms
description: Platform-specific guides, setup, and reference for Claude, OpenAI, Gemini, M365 Copilot, and Cursor
---Platform-specific setup guides, topics, and Q&A organized by AI platform.

## Choose Your Platform

<style>
.platform-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  border: 1px solid var(--sl-color-gray-5);
  border-radius: 8px;
  overflow: hidden;
}
:root[data-theme='light'] .platform-list { border-color: #d4d4d0; }
.platform-row {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--sl-color-gray-5);
  background: var(--sl-color-gray-6);
}
.platform-row:last-child { border-bottom: none; }
:root[data-theme='light'] .platform-row { background: #fff; border-bottom-color: #eaeae6; }
.platform-row strong { flex-shrink: 0; min-width: 9rem; font-size: 0.95rem; }
.platform-row span { flex: 1; font-size: 0.88rem; color: var(--sl-color-gray-2); line-height: 1.5; }
.platform-row a { flex-shrink: 0; font-size: 0.85rem; font-weight: 600; color: var(--sl-color-accent) !important; text-decoration: none !important; white-space: nowrap; }
.platform-row a:hover { text-decoration: underline !important; }
:root[data-theme='light'] .platform-row a { color: #282828 !important; }
@media (max-width: 600px) {
  .platform-row { flex-direction: column; gap: 0.25rem; }
  .platform-row strong { min-width: unset; }
}
</style>

<div class="platform-list">
  <div class="platform-row">
    <strong>Claude</strong>
    <span>Anthropic's Claude models, Claude Code CLI, and MCP integrations</span>
    <a href="claude/">Claude guides →</a>
  </div>
  <div class="platform-row">
    <strong>OpenAI / ChatGPT</strong>
    <span>GPT models, Assistants API, and function calling</span>
    <a href="openai/">OpenAI guides →</a>
  </div>
  <div class="platform-row">
    <strong>Google Gemini</strong>
    <span>Gemini models and Vertex AI</span>
    <a href="google-gemini/">Gemini guides →</a>
  </div>
  <div class="platform-row">
    <strong>M365 Copilot</strong>
    <span>Microsoft 365 Copilot and Azure OpenAI</span>
    <a href="m365-copilot/">M365 Copilot guides →</a>
  </div>
  <div class="platform-row">
    <strong>Cursor</strong>
    <span>AI-native code editor with deep skill support across Claude, Codex, and other models</span>
    <a href="cursor/">Cursor guides →</a>
  </div>
</div>
