# Claude API (Messages API MCP connector)

The Messages API can call a remote MCP server directly, with no MCP client of
your own. It sends `authorization_token` as `Authorization: Bearer <token>`.

Requires the beta header `mcp-client-2025-11-20`. You need **both** halves:
the server in `mcp_servers` and an `mcp_toolset` entry in `tools` that names
it.

## Python

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
export FLEXCONNECT_MCP_TOKEN=flx_...
```

```python
import os
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    betas=["mcp-client-2025-11-20"],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://mcp.audesseinc.com/mcp/",
            "name": "flexconnect-telemetry",
            "authorization_token": os.environ["FLEXCONNECT_MCP_TOKEN"],
        }
    ],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "flexconnect-telemetry"}],
    messages=[{"role": "user", "content": "List my devices and their latest battery voltage."}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
```

## cURL

```bash
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: mcp-client-2025-11-20" \
  -d '{
    "model": "claude-opus-5-5",
    "max_tokens": 16000,
    "messages": [{"role": "user", "content": "List my devices."}],
    "mcp_servers": [{
      "type": "url",
      "url": "https://mcp.audesseinc.com/mcp/",
      "name": "flexconnect-telemetry",
      "authorization_token": "'"$FLEXCONNECT_MCP_TOKEN"'"
    }],
    "tools": [{"type": "mcp_toolset", "mcp_server_name": "flexconnect-telemetry"}]
  }'
```

## Notes

- To expose only some tools, use the toolset's allowlist/denylist options.
  See the [MCP connector docs](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector).
- In a multi-tenant app, pass **each end user's own** API key, never a shared
  admin key. The server scopes results to the token's org and devices.
- The MCP connector isn't eligible for zero data retention.
