# ChatGPT

ChatGPT connects to custom MCP servers with **OAuth**. You sign in with your
Flexconnect account, and ChatGPT only sees the devices your account can
access.

## Setup

1. **Workspaces (Business / Enterprise / Edu):** an admin enables developer
   mode / custom MCP under **Workspace Settings → Permissions & Roles**. On
   **Pro**, turn developer mode on in your own settings.
2. Go to **Plugins** (<https://chatgpt.com/plugins>), select **+**, then
   **Add custom MCP server**.
3. Name: `Flexconnect Telemetry`. Under **Connection**, set **Server URL** to
   `https://mcp.audesseinc.com/mcp/`.
4. Authentication: **OAuth**. Leave the client ID empty. ChatGPT registers
   itself with the server.
5. Accept the risk warning (**I understand and want to continue**), then
   **Create as a plugin**.
6. Install the plugin, then enable it in a conversation. You'll be asked to
   sign in with your Flexconnect account.

ChatGPT's menu labels change often. If these don't match, see OpenAI's
[Add custom MCP server](https://developers.openai.com/api/docs/guides/custom-mcp-server)
guide.

## Using it

Ask e.g. "List my Flexconnect devices and summarize their latest overview."
All telemetry tools are read-only.

If sign-in fails or the plugin stops working, disconnect it in ChatGPT's
plugin settings and connect again.
