# Claude (claude.ai, Claude Desktop, Claude mobile)

claude.ai calls MCP servers **custom connectors**. A connector you add on the
web also works in Claude Desktop and the mobile apps. You sign in with your
Flexconnect account, so there's no token to paste, and the connector only
sees the devices your account can access.

## Free, Pro, or Max

1. Go to **Customize > Connectors** (<https://claude.ai/customize/connectors>).
2. Click **Add custom connector**.
3. Name: `Flexconnect Telemetry`.
   MCP server URL: `https://mcp.audesseinc.com/mcp/`
4. Leave the OAuth client ID and secret empty. Claude registers itself with
   the server.
5. Click **Add**, then **Connect**, and sign in with your Flexconnect account.

The Free plan allows one custom connector.

## Team or Enterprise

An Owner adds the connector for the whole organization:

1. Go to **Organization settings > Connectors**
   (<https://claude.ai/admin-settings/connectors>).
2. Select **Add**, then **Custom** (choose **Web** if asked for a type).
3. Enter the name and URL as above, then **Add**.
4. Members enable it under **Customize > Connectors** (it has the **Custom**
   label), click **Connect**, and sign in with their own Flexconnect account.

Each member gets their own access. Nobody shares a key.

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
- **Leave the OAuth client fields empty** unless Audesse gave you a client
  ID.

**Sign-in fails or the connector stops working**

Under **Customize > Connectors**, open **Flexconnect Telemetry**, disconnect,
and click **Connect** again.

To check that the server is up from a terminal (it should print `401`, which
means it's asking for sign-in):

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://mcp.audesseinc.com/mcp/ \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Using an API key instead

If you'd rather use a Flexconnect API key (`flx_...`), and your org has the
**Request headers** beta:

1. Add the custom connector as above, but set Authentication to **No
   sign-in**.
2. Open **Request headers** and add header `authorization` with value
   `Bearer flx_...` (**include `Bearer ` and the space**), marked
   **Required**.

On Team and Enterprise, every member shares the key the Owner entered, so
scope it to what the whole Claude org should see. To rotate the key, remove
the connector and add it again.
