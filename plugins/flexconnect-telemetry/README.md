# flexconnect-telemetry

Registers the Flexconnect telemetry MCP server
(`https://mcp.audesseinc.com/mcp/`, Streamable HTTP) in your coding agent,
plus a skill that teaches the agent how to use it.

Tools (all read-only, scoped to whatever org/devices your token is authorized
for):

`telemetry_list_devices`, `telemetry_list_fields`, `telemetry_get_overview`,
`telemetry_get_last`, `telemetry_get_multi_last`, `telemetry_get_range`,
`telemetry_get_multi_range`.

## Contents

| File | Read by |
| - | - |
| `.claude-plugin/plugin.json` + `.mcp.json` | Claude Code |
| `plugin.json` + `mcp.json` (Agent Plugins 1.0) | Codex, GitHub Copilot |
| `.cursor-plugin/plugin.json` + `cursor.mcp.json` | Cursor |
| `skills/flexconnect-telemetry/SKILL.md` | all four |

## 1. Get a token

The server accepts a Flexconnect API key (`flx_...`) or a Flexconnect JWT as
`Authorization: Bearer <token>`.

We recommend an API key: create one in the Flexconnect dashboard, scoped to
the devices the agent should see, with `telemetry:read`.

Treat the token like a password. It grants read access to your org's
telemetry.

## 2. Install

Replace `Audesse/flexconnect-plugins` with a local path to this repo if you're
working from a checkout.

### Claude Code

```bash
/plugin marketplace add Audesse/flexconnect-plugins
/plugin install flexconnect-telemetry@flexconnect-plugins
```

Non-interactive: `claude plugin install flexconnect-telemetry@flexconnect-plugins --scope user`.

When prompted for **Flexconnect MCP token**, paste the token. It's stored
securely, and `.mcp.json` adds the `Bearer ` prefix. If you skipped the prompt,
set it later with `/config`. Run `/reload-plugins` if asked.

Tools show up as `mcp__plugin_flexconnect-telemetry_telemetry__<tool>`.

### Codex

```bash
codex plugin marketplace add Audesse/flexconnect-plugins
```

Then install **Flexconnect Telemetry** from the Plugins directory (Codex app /
ChatGPT desktop). Codex asks for the API key during install (`mcp.json`
declares bearer `api_key` auth).

### GitHub Copilot CLI

```bash
copilot plugin marketplace add Audesse/flexconnect-plugins
copilot plugin install flexconnect-telemetry@flexconnect-plugins
```

The portable `mcp.json` deliberately carries no credentials (the Agent Plugins
spec forbids secrets in headers), so authentication is up to Copilot. If the
server shows as failing to connect, add it manually with a bearer header
instead — see [docs/connect/manual-mcp-config.md](../../docs/connect/manual-mcp-config.md#github-copilot-cli).

### Cursor

Add this repo as a team marketplace (Dashboard → Plugins), or install from
the Cursor Marketplace once published. Set the `FLEXCONNECT_MCP_TOKEN`
variable to your token when prompted / in the dashboard.

## Other clients

To connect the same server to claude.ai, ChatGPT, the Claude API or the OpenAI
API, see [docs/connect](../../docs/connect/README.md).
