# Connecting AI clients to the Flexconnect API

The Flexconnect MCP server is a remote **Streamable HTTP** MCP endpoint at
`https://mcp.audesseinc.com/mcp/`. It accepts two kinds of authentication:

- **OAuth sign-in** with your Flexconnect account. Clients that support it
  (the plugins, claude.ai, ChatGPT) discover it automatically, so there's nothing
  to configure.
- **A bearer token**: a Flexconnect API key (`flx_...`) or JWT sent as
  `Authorization: Bearer <your token>`. Use this for the APIs and clients
  without OAuth.

How to get a token: [plugin README § Using a token instead](../../plugins/flexconnect-telemetry/README.md#using-a-token-instead).

## Which guide?

| Client | Works today? | Guide |
| - | - | - |
| Claude Code, Codex, Cursor | Yes, install the plugin and sign in with OAuth | [plugin README](../../plugins/flexconnect-telemetry/README.md) |
| GitHub Copilot, or any of the above without the plugin | Yes, manual MCP config | [manual-mcp-config.md](manual-mcp-config.md) |
| claude.ai (web, Desktop, mobile) | Yes, sign in with OAuth | [claude.md](claude.md) |
| ChatGPT (web/desktop) | Yes, sign in with OAuth | [chatgpt.md](chatgpt.md) |
| Claude API (Messages API) | Yes | [claude-api.md](claude-api.md) |
| OpenAI API (Responses API) | Yes | [openai-api.md](openai-api.md) |

## Security notes

- Tokens grant read access to your org's telemetry. Prefer API keys scoped to
  specific devices, give each client its own key, and revoke keys you no
  longer use.
- Never commit a token. Use the client's secret storage, an environment
  variable, or a password prompt.
