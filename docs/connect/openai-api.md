# OpenAI API (Responses API remote MCP tool)

The Responses API can call a remote MCP server as a tool. Pass the Flexconnect
token in `authorization`. OpenAI doesn't store it, so send it on every request.

## Python

```bash
pip install openai
export OPENAI_API_KEY=sk-...
export FLEXCONNECT_MCP_TOKEN=flx_...
```

```python
import os
from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-6-astra",
    tools=[
        {
            "type": "mcp",
            "server_label": "flexconnect_telemetry",
            "server_url": "https://mcp.audesseinc.com/mcp/",
            "authorization": os.environ["FLEXCONNECT_MCP_TOKEN"],
            "require_approval": "never",
        }
    ],
    input="List my devices and their latest battery voltage.",
)

print(resp.output_text)
```

## cURL

```bash
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-6-astra",
    "tools": [{
      "type": "mcp",
      "server_label": "flexconnect_telemetry",
      "server_url": "https://mcp.audesseinc.com/mcp/",
      "authorization": "'"$FLEXCONNECT_MCP_TOKEN"'",
      "require_approval": "never"
    }],
    "input": "List my devices."
  }'
```

## Notes

- `require_approval: "never"` is reasonable here because every telemetry tool
  is read-only. Use `"always"` for servers with write tools, and answer the
  resulting `mcp_approval_request` items.
- `allowed_tools: ["telemetry_get_overview", ...]` limits which tools are
  imported, which cuts latency and cost.
- In a multi-tenant app, pass each end user's own API key.
