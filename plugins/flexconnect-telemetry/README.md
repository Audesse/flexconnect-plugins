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
| `.codex-plugin/plugin.json` + `codex.mcp.json` | Codex |
| `.cursor-plugin/plugin.json` + `cursor.mcp.json` | Cursor |
| `skills/flexconnect-telemetry/SKILL.md` | all clients |

## 1. Sign in

Claude Code, Codex and Cursor sign you in with OAuth: the first time the
agent uses the server, a browser window opens and you sign in with your
Flexconnect account. There's no token to paste, and the agent only sees the
devices your account can access.

### Using a token instead

Clients without OAuth (GitHub Copilot, the Claude and OpenAI APIs) need a
Flexconnect API key (`flx_...`) or JWT, sent as
`Authorization: Bearer <token>`. Create an API key in the Flexconnect
dashboard, scoped to the devices the agent should see, with
`telemetry:read`. Treat it like a password.

## 2. Install

Replace `Audesse/flexconnect-plugins` with a local path to this repo if you're
working from a checkout.

### Claude Code

```bash
/plugin marketplace add Audesse/flexconnect-plugins
/plugin install flexconnect-telemetry@flexconnect-plugins
```

Non-interactive: `claude plugin install flexconnect-telemetry@flexconnect-plugins --scope user`.

Run `/reload-plugins` if asked. Then run `/mcp`, select
`plugin:flexconnect-telemetry:telemetry` (marked **Needs authentication**),
and sign in with your Flexconnect account. From a shell:
`claude mcp login plugin:flexconnect-telemetry:telemetry`.

Tools show up as `mcp__plugin_flexconnect-telemetry_telemetry__<tool>`.

### Codex

```bash
codex plugin marketplace add Audesse/flexconnect-plugins
```

Then install **Flexconnect Telemetry** from the Plugins directory (Codex app /
ChatGPT desktop).

Codex signs you in with OAuth, so there's no token to paste. When asked,
sign in with your Flexconnect account in the browser window that opens. To
sign in again later, run:

```bash
codex mcp login telemetry
```

`codex mcp list` should show `telemetry` with Auth `OAuth` once you're
signed in.

### GitHub Copilot CLI

```bash
copilot plugin marketplace add Audesse/flexconnect-plugins
copilot plugin install flexconnect-telemetry@flexconnect-plugins
```

The plugin adds the skill. Copilot plugins have no way to supply the token,
so add the MCP server itself with a bearer header, as described in
[docs/connect/manual-mcp-config.md](../../docs/connect/manual-mcp-config.md#github-copilot-cli).

### Cursor

Add this repo as a team marketplace (Dashboard → Plugins), or install from
the Cursor Marketplace once published. In **Settings → MCP**, click
**Connect** next to `telemetry` and sign in with your Flexconnect account.

## Other clients

To connect the same server to claude.ai, ChatGPT, the Claude API or the OpenAI
API, see [docs/connect](../../docs/connect/README.md).
