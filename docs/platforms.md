# Client plugin formats

Notes on how each client loads plugins from this repo, as of 2026-10. The
formats are moving fast. Check the linked docs when something stops loading.

## Claude Code

- Marketplace: `.claude-plugin/marketplace.json`. Plugin manifest:
  `<plugin>/.claude-plugin/plugin.json`. MCP: `<plugin>/.mcp.json`.
- `.mcp.json` supports `${VAR}`, `${VAR:-default}` and
  `${user_config.<key>}` interpolation in `url` and `headers`.
- Secrets: declare in `userConfig` with `"sensitive": true`. Claude Code
  prompts on install and stores the value in secure storage.
- Remote transport type is `"http"`.
- Validate with `claude plugin validate <path>`.
- Docs: <https://code.claude.com/docs/en/plugins>

## Codex

- Marketplace: `.agents/plugins/marketplace.json`. `source` is an object
  (`{"source": "local", "path": "./plugins/x"}`, resolved from the repo
  root). Every entry needs `policy` and `category`.
- Manifest: `<plugin>/.codex-plugin/plugin.json`, with `interface` at the top
  level and `mcpServers` pointing at `codex.mcp.json`.
- `codex.mcp.json` uses Codex's own server keys (the same as
  `[mcp_servers.*]` in `config.toml`). We give only `url` and
  `scopes: ["telemetry:read"]`. Codex discovers OAuth from the server's 401
  `WWW-Authenticate` header, registers a client dynamically, and runs the
  PKCE login on install (`policy.authentication: ON_INSTALL`) or with
  `codex mcp login <server>`. For a static token, use
  `bearer_token_env_var` instead. `bearer_token` (a literal token) is
  rejected.
- Don't set `oauth_resource` to the URL with a trailing slash: Codex then
  sends two `resource` parameters (`.../mcp` and `.../mcp/`).
- **Don't ship a root Agent Plugins `plugin.json`.** When one exists, Codex
  uses it and its `mcp.json`, and ignores the MCP config in
  `.codex-plugin/`. Codex 26.1007 also rejects the documented per-server
  `extensions["com.openai"].auth` block in `mcp.json` ("unknown field
  `extensions`"), so a portable manifest can't carry auth settings yet.
- Check an install with `codex mcp list`: the server shows `Not logged in`
  until the user signs in, then `OAuth`. Plugin load errors are logged to
  `~/.codex/logs_2.sqlite` (target `codex_core_plugins::loader`).
- Docs: <https://developers.openai.com/codex/plugins/build>

## GitHub Copilot (CLI and VS Code)

- Marketplace: `.github/plugin/marketplace.json` (also reads
  `.claude-plugin/marketplace.json`). Same schema as Claude Code's.
- Copilot reads Agent Plugins 1.0 manifests at the plugin root and falls back
  to legacy manifest locations. We don't ship a portable manifest (see
  Codex), so Copilot uses the fallback.
- Copilot plugins can't supply a bearer token, so users add the server with
  [manual config](connect/manual-mcp-config.md#github-copilot-cli).
- Docs: <https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating>

## Cursor

- Marketplace: `.cursor-plugin/marketplace.json` (same shape as Claude
  Code's: `name`, `owner`, `plugins[].source`).
- Manifest: `<plugin>/.cursor-plugin/plugin.json`. Its `mcpServers` field
  overrides the default `mcp.json` discovery. We point it at
  `cursor.mcp.json`, because the root `mcp.json` is the portable file and
  has no auth header.
- Secrets: declare a JSON-schema `variables` object in the manifest and
  reference it as `${NAME}` in the MCP file. Values are set in the Cursor
  dashboard. Cursor plugins don't support `${env:NAME}`, which only works in
  a user's own `.cursor/mcp.json`.
- Transport is inferred from `url`/`command`, so omit `type`.
- Docs: <https://cursor.com/docs/plugins>, <https://cursor.com/docs/reference/plugins>
