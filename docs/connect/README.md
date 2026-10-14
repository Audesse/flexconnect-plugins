# Connecting AI clients to the Flexconnect API

The Flexconnect MCP server is a remote **Streamable HTTP** MCP endpoint. Send
a Flexconnect API key (`flx_...`) or a Flexconnect JWT as a bearer token:

```
URL:     https://mcp.audesseinc.com/mcp/
Header:  Authorization: Bearer <your token>
```

How to get a token: [plugins/flexconnect-telemetry/README.md § Get a token](../../plugins/flexconnect-telemetry/README.md#1-get-a-token).

## Which guide?

| Client | Works today? | Guide |
| - | - | - |
| Claude Code, Codex, Copilot, Cursor | Yes, install the plugin | [plugin README](../../plugins/flexconnect-telemetry/README.md) |
| Claude Code / Codex / Copilot / Cursor without the plugin | Yes, manual MCP config | [manual-mcp-config.md](manual-mcp-config.md) |
| claude.ai (web, Desktop, mobile) | Yes, if your org has the **Request headers** beta | [claude.md](claude.md) |
| ChatGPT (web/desktop) | **No, not yet** | [chatgpt.md](chatgpt.md) |
| Claude API (Messages API) | Yes | [claude-api.md](claude-api.md) |
| OpenAI API (Responses API) | Yes | [openai-api.md](openai-api.md) |

## Security notes

- Tokens grant read access to your org's telemetry. Prefer API keys scoped to
  specific devices, give each client its own key, and revoke keys you no
  longer use.
- Never commit a token. Use the client's secret storage, an environment
  variable, or a password prompt.
