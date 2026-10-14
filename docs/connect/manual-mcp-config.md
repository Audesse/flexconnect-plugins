# Manual MCP configuration (without the plugin)

Use these if you can't install the plugin, or the plugin's auth flow doesn't
work in your client. Keep the token in an environment variable or secret
prompt, not in a committed file:

```bash
export FLEXCONNECT_MCP_TOKEN=flx_...
```

## Claude Code

```bash
claude mcp add --transport http --scope user flexconnect-telemetry \
  https://mcp.audesseinc.com/mcp/ \
  --header "Authorization: Bearer $FLEXCONNECT_MCP_TOKEN"
```

(This writes the expanded token into `~/.claude.json`. The plugin keeps it in
secure storage instead.)

## Codex (`~/.codex/config.toml`)

```toml
[mcp_servers.flexconnect-telemetry]
url = "https://mcp.audesseinc.com/mcp/"
bearer_token_env_var = "FLEXCONNECT_MCP_TOKEN"
```

## Cursor (`~/.cursor/mcp.json` or `.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "flexconnect-telemetry": {
      "url": "https://mcp.audesseinc.com/mcp/",
      "headers": { "Authorization": "Bearer ${env:FLEXCONNECT_MCP_TOKEN}" }
    }
  }
}
```

## GitHub Copilot in VS Code (`.vscode/mcp.json`)

VS Code prompts for the token once and stores it securely:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "flexconnect-token",
      "description": "Flexconnect API key (flx_...)",
      "password": true
    }
  ],
  "servers": {
    "flexconnect-telemetry": {
      "type": "http",
      "url": "https://mcp.audesseinc.com/mcp/",
      "headers": { "Authorization": "Bearer ${input:flexconnect-token}" }
    }
  }
}
```

## GitHub Copilot CLI

Run `/mcp add` inside `copilot`, choose **HTTP**, enter the URL, and add the
header `Authorization: Bearer flx_...`. This saves the server to
`~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "flexconnect-telemetry": {
      "type": "http",
      "url": "https://mcp.audesseinc.com/mcp/",
      "headers": { "Authorization": "Bearer flx_..." },
      "tools": ["*"]
    }
  }
}
```
