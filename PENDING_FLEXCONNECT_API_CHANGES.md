# Pending flexconnect-api changes

## Annotation tools: the connect guides still say the tools are read-only

flexconnect-api's MCP server now has three annotation tools, two of which
write: `telemetry_list_annotations` (read-only), `telemetry_create_annotation`
and `telemetry_delete_annotation` (the first non-read-only tools; delete is
destructive). Writes need the `device:metadata:write` key permission (JWTs are
always allowed). OAuth clients (ChatGPT, claude.ai, Gemini) can now get
annotation writes too: the derived key gets `device:metadata:write` only if
the client requested it in `scope` and the key the user pasted holds it;
otherwise it stays read-only (see the scope entry below). The OAuth
consent page and token `scope` reflect this.

The plugin README, skills and version were already updated. Still to do in
`docs/connect/`:

- `chatgpt.md` (line ~30): "All telemetry tools are read-only." Say the
  annotation create/delete tools write, and that they work only if the pasted
  key has `device:metadata:write`.
- `claude.md` (line ~39): same wording fix.
- `openai-api.md` (line ~59): the `require_approval` advice assumes a
  read-only server; recommend approval for the write tools.
- Also check `claude-api.md` and `manual-mcp-config.md` for the same
  assumption, and the OAuth steps (a key with `device:metadata:write` is
  needed to get annotation writes).

`telemetry_create_annotation(device_id, text, timestamp=None)`: the timestamp
is optional (the server's current time is used when omitted); note `text`
comes before `timestamp`.

Behaviour change worth knowing: the legacy `insert_annotation` command on
`POST /api/command` now rejects text over 128 characters (400) and stores in
the same place annotations are read from.

## OAuth: annotation writes now need `device:metadata:write` in `scope`

The MCP OAuth flow now grants only the scopes the client requests. With no
`scope` (or an empty one) the connected app gets `telemetry:read` only, even
if the API key the user pasted can write. To get annotation writes
(`telemetry_create_annotation` and delete), the client must request
`device:metadata:write` in the `scope` parameter at `/oauth/authorize`
(`telemetry:read` is always included). The grant is still capped by the pasted
key: if it lacks `device:metadata:write`, the write is silently dropped and the
token response `scope` says what was granted.

Do: update the `docs/connect/` guides (`chatgpt.md`, `claude.md`, any others
that describe OAuth) to say writes need `device:metadata:write` requested as a
scope, and add a scope setting to `plugins/flexconnect-telemetry/.mcp.json`
(and any other plugin MCP configs) if the client supports one. Clients that
cannot set a scope stay read-only.
