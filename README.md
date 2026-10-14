# Flexconnect plugins

Agent plugins and MCP extensions for Audesse Flexconnect, packaged for
**Claude Code**, **OpenAI Codex**, **GitHub Copilot** and **Cursor** from one
repo, with guides for connecting the same servers to **claude.ai**,
**ChatGPT**, and the **Claude** and **OpenAI** APIs.

## Plugins

| Plugin | What it does |
| - | - |
| [`flexconnect-telemetry`](plugins/flexconnect-telemetry/) | Read-only access to your org's Flexconnect device telemetry (device list, overview, latest values, time ranges) via the Flexconnect MCP server |

## Install

This repo is a plugin marketplace for each client:

```bash
# Claude Code
/plugin marketplace add Audesse/flexconnect-plugins
/plugin install flexconnect-telemetry@flexconnect-plugins

# Codex (then install from the Plugins directory)
codex plugin marketplace add Audesse/flexconnect-plugins

# GitHub Copilot CLI
copilot plugin marketplace add Audesse/flexconnect-plugins
copilot plugin install flexconnect-telemetry@flexconnect-plugins

# Cursor: add the repo as a team marketplace in the Cursor dashboard
```

Each plugin's README covers its token and per-client setup.

## Connect other AI apps

[docs/connect](docs/connect/README.md) has step-by-step guides for:

- [Claude: claude.ai, Desktop, mobile](docs/connect/claude.md)
- [ChatGPT](docs/connect/chatgpt.md)
- [Claude API](docs/connect/claude-api.md) · [OpenAI API](docs/connect/openai-api.md)
- [Manual MCP config](docs/connect/manual-mcp-config.md) for Claude Code, Codex, Cursor and Copilot (VS Code and CLI)

## Layout

```
.claude-plugin/marketplace.json    Claude Code marketplace (Copilot also reads it)
.github/plugin/marketplace.json    GitHub Copilot marketplace
.cursor-plugin/marketplace.json    Cursor marketplace
.agents/plugins/marketplace.json   Codex marketplace
plugins/<name>/                    one directory per plugin, all clients
docs/platforms.md                  per-client file formats
docs/connect/                      connection guides for chat apps and APIs
scripts/validate.py                consistency checks (run in CI)
```

Adding or changing a plugin? Read [AGENTS.md](AGENTS.md).
