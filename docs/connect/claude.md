# Claude (claude.ai, Claude Desktop, Claude mobile)

claude.ai calls MCP servers **custom connectors**. A connector you add on the
web also works in Claude Desktop and the mobile apps.

> **Requirement:** claude.ai sends your token through **Request headers**.
> That feature is in beta and only available to some organizations. If the
> **Add custom connector** dialog has no **Request headers** section, your org
> doesn't have it yet. Use [Claude Code](../../plugins/flexconnect-telemetry/README.md)
> or the [Claude API](claude-api.md) instead.

## Free, Pro, or Max

1. Go to **Customize > Connectors** (<https://claude.ai/customize/connectors>).
2. Click **Add custom connector**.
3. Name: `Flexconnect Telemetry`.
   MCP server URL: `https://mcp.audesseinc.com/mcp/`
4. Authentication: choose **No sign-in**.
5. Open **Request headers** and add:
   - Header name: `authorization`
   - Value: `Bearer flx_...` (**include `Bearer ` and the space**. Claude sends
     the value exactly as entered.)
   - Mark it **Required**.
6. Click **Add**.

The Free plan allows one custom connector.

## Team or Enterprise

An Owner adds the connector for the whole organization:

1. Go to **Organization settings > Connectors**
   (<https://claude.ai/admin-settings/connectors>).
2. Select **Add**, then **Custom** (choose **Web** if asked for a type).
3. Enter the URL and request header as above, then **Add**.
4. Members enable it under **Customize > Connectors** (it has the **Custom**
   label) and click **Connect**.

**Every member shares the header value the Owner entered.** Use an API key
scoped to exactly what the whole Claude org should see, not a personal key.

## Using it

- In a chat, click **+** → **Connectors** and toggle **Flexconnect
  Telemetry** on.
- Ask e.g. "Which of my Flexconnect devices reported low battery in the last 24 hours?"
- Under **Customize > Connectors**, you can set per-tool permissions. All
  telemetry tools are read-only.

## Troubleshooting

**"Couldn't connect to the server. Check that the URL points to a valid MCP
server."**

- **Check the URL.** It should be `https://mcp.audesseinc.com/mcp/` (the
  trailing slash is optional).
- **Authentication must be "No sign-in".** The token goes in **Request
  headers**, not through a sign-in flow.

To check the server from a terminal (it should print `200`):

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://mcp.audesseinc.com/mcp/ \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"curl","version":"0"}}}'
```

## Changing the token

Authentication settings can't be edited. To rotate the key, remove the
connector and add it again (members reconnect afterwards).

## Claude Desktop with a local bridge (fallback)

If your org lacks the Request headers beta, Claude Desktop can still reach the
server through a local stdio bridge. In **Settings > Developer > Edit
Config** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "flexconnect-telemetry": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote", "https://mcp.audesseinc.com/mcp/",
        "--header", "Authorization:${FLEXCONNECT_AUTH}"
      ],
      "env": { "FLEXCONNECT_AUTH": "Bearer flx_..." }
    }
  }
}
```

This needs Node.js, stores the token in plain text in that file, and is
desktop-only. `mcp-remote` is a third-party package. Restart Claude Desktop
after saving.
