---
title: API
description: The API building block — programmatic interfaces for accessing AI models and cloud services, the code-first way to interact with AI
---

# API

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What an API Is

An **API** (Application Programming Interface) is the code-first way to interact with AI. Instead of typing in a chat window, you send a structured request to a service and get a structured response back. APIs let you integrate AI capabilities into applications, automate workflows programmatically, and access model capabilities beyond what the chat UI provides.

Every major AI platform exposes its models through APIs. The same model you chat with in a browser can be called from a Python script, a web application, or an automated pipeline — with full control over parameters, inputs, and outputs.

## Key Characteristics

- **Stateless request/response pattern** — send a request with your input, get a response with the output; each call is independent unless you manage state yourself
- **Authentication via API keys** — access is controlled by secret keys tied to your account, with usage tracked and billed per call
- **Platform-agnostic** — any programming language that can make HTTP requests can call an API; no vendor lock-in at the protocol level
- **Metered by usage** — billed by tokens processed, API calls made, or compute consumed, giving fine-grained cost control

## When to Use It

Use APIs when:

- You need to integrate AI into an existing application or product
- You're automating a workflow that runs programmatically (batch processing, scheduled tasks, pipelines)
- You need control over parameters the chat UI doesn't expose (temperature, max tokens, structured outputs)
- You're building a product or internal tool powered by AI
- You need to process data at scale (hundreds or thousands of inputs)

## Example

Calling the Claude API from a Python script to classify 1,000 customer support tickets overnight — each ticket gets sent as a request with classification instructions, and the response contains the category, priority, and a brief summary. No human sits at a chat window; the script runs unattended and writes results to a database.

Or calling a search API to enrich an agent's research — the agent programmatically queries Google, retrieves results, and synthesizes them into a report.

## Types of APIs

APIs aren't limited to AI models. A typical AI workflow might call several types:

| API Type | What It Does | Examples |
|----------|-------------|----------|
| **Model APIs** | Send prompts to AI models and receive generated responses | Anthropic API, OpenAI API, Google Gemini API |
| **Cloud service APIs** | Access platform capabilities like search, translation, or storage | Google Search API, AWS Translate, Azure Cognitive Services |
| **Third-party service APIs** | Read from and write to business tools | Slack API, GitHub API, HubSpot API, Notion API |
| **Data APIs** | Query databases or data warehouses | BigQuery API, Snowflake API, Elasticsearch API |

## Key Concepts

**Endpoints** — The specific URL you send requests to. Each capability has its own endpoint (e.g., `/messages` for sending a prompt, `/embeddings` for generating vector representations).

**Authentication** — Most APIs require an API key sent in the request header. Keys are tied to your account and control access, rate limits, and billing.

**Request/response format** — APIs typically use JSON. You send a structured request (model, messages, parameters) and receive a structured response (generated text, metadata, usage stats).

**Rate limits** — APIs limit how many requests you can make per minute or per day to ensure fair usage. Production applications need to handle rate limiting gracefully.

**Streaming** — For long responses, many APIs support streaming — sending the response back in chunks as it's generated, rather than waiting for the full response.

**Structured outputs** — Many model APIs can return responses in a specified JSON schema, making it easy to parse results programmatically without brittle text extraction.

## Platform Implementations

| Platform | How It Works | API Reference |
|----------|-------------|---------------|
| **Claude (Anthropic API)** | REST API with Messages endpoint; Python and TypeScript SDKs available; supports streaming, tool use, and vision | <a href="https://docs.anthropic.com/en/home" target="_blank">Docs</a> · <a href="https://docs.anthropic.com/en/api" target="_blank">API Reference</a> |
| **OpenAI API** | REST API with Chat Completions and Responses endpoints; Python and TypeScript SDKs available; supports streaming, function calling, and structured outputs | <a href="https://developers.openai.com/api/docs/" target="_blank">Docs</a> · <a href="https://developers.openai.com/api/reference/" target="_blank">API Reference</a> |
| **Google (Gemini API / Vertex AI)** | REST API with generateContent endpoint; Python SDK available; Vertex AI adds enterprise features and additional model access | <a href="https://ai.google.dev/gemini-api/docs" target="_blank">Gemini API Docs</a> · <a href="https://ai.google.dev/api" target="_blank">API Reference</a> |
| **Azure AI Services** | REST APIs for OpenAI models (via Azure OpenAI) and cognitive services (vision, speech, language); .NET, Python, Java SDKs | <a href="https://learn.microsoft.com/en-us/azure/ai-services" target="_blank">Docs</a> · <a href="https://learn.microsoft.com/en-us/rest/api/aiservices/" target="_blank">API Reference</a> |

## Relationship to Other Blocks

API is the programmatic bridge between your code and AI capabilities:

- **Model** is accessed through APIs — the API is how you call the model from code
- **Prompts** are sent as structured messages in API requests
- **Context** is included as system messages, file attachments, or retrieved data in API calls
- **Skills** can wrap API calls into reusable routines
- **Agents** use APIs to call models, tools, and services as part of their autonomous execution
- **MCP** servers often wrap APIs — providing a standard interface for agents to call external services
- **SDKs** provide higher-level abstractions over raw API calls, handling orchestration, retries, and tool use patterns

## Related

- [Agentic Building Blocks](../index.md) — API in the context of all ten building blocks
- [SDK](../sdk/index.md) — frameworks that provide higher-level abstractions over APIs
- [MCP](../mcp/index.md) — the protocol that connects AI to external systems (often backed by APIs)
- [Agents](../agents/index.md) — autonomous systems that use APIs to call models and tools
- [AI Use Cases](../../use-cases/index.md) — what teams build with these blocks
- [Coding Use Cases](../../use-cases/coding/index.md) — code-first AI workflows that rely on APIs
- [Automation Use Cases](../../use-cases/automation/index.md) — automated pipelines built on API calls
- [Platforms](../../platforms/index.md) — platform-specific API guides
