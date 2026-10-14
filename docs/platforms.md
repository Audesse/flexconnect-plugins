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

## Agent Plugins 1.0 (portable): Codex, GitHub Copilot

- Spec: <https://agent-plugins.org/specification>
- Manifest: `<plugin>/plugin.json` with
  `"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"`.
  Allowed top-level fields: `$schema`, `name`, `version`, `description`,
  `author`, `homepage`, `repository`, `license`, `keywords`, `extensions`.
- MCP: `<plugin>/mcp.json` with
  `"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"`.
  Remote servers need `"type": "streamable-http"` (or `"sse"`).
- **No interpolation in `url`/`headers`, and no secrets in headers.** Auth is
  client-managed. Client-specific extensions go under `extensions`, keyed by
  reverse-domain namespace.
- Skills are discovered from `skills/`. No manifest field is needed.

### Codex

- Marketplace: `.agents/plugins/marketplace.json`. `source` is an object
  (`{"source": "local", "path": "./plugins/x"}`, resolved from the repo
  root). Every entry needs `policy` and `category`.
- Bearer-token auth: on the server in `mcp.json`, set
  `extensions["com.openai"].auth = {"type": "api_key", "headerScheme": "bearer"}`.
  Codex asks the user for the key during install (`policy.authentication:
  ON_INSTALL`).
- OpenAI-specific manifest fields go under `extensions["com.openai"]`
  (`interface`, `hooks`, `apps`, ...). A legacy `.codex-plugin/plugin.json`
  is still read as a fallback, but we don't ship one.
- Docs: <https://developers.openai.com/codex/plugins/build>

### GitHub Copilot (CLI and VS Code)

- Marketplace: `.github/plugin/marketplace.json` (also reads
  `.claude-plugin/marketplace.json`). Same schema as Claude Code's.
- Loads the Agent Plugins `plugin.json` + `mcp.json`. Copilot-specific
  components go in `<plugin>/com.github.copilot/`.
- **Known gap:** we haven't confirmed how Copilot supplies a static bearer
  token to an Agent Plugins remote server. If it doesn't, users fall back to
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
