---
name: flexconnect-telemetry
description: Answer questions about Flexconnect devices (location, battery, sensor readings, trends over time) using the Flexconnect telemetry MCP tools. Use when the user asks about their Flexconnect devices, fleet, or telemetry data.
---

# Querying Flexconnect telemetry

The `telemetry` MCP server is read-only and scoped to the caller's own org and
devices. All timestamps are ISO-8601 UTC (`2024-01-01T00:00:00Z`).

## Workflow

1. **Find the device.** Call `telemetry_list_devices` to map the alias the user
   mentions ("device 12") to a `device_id`. Don't guess ids.
2. **Find the field names.** Call `telemetry_list_fields` with the `device_id`
   before asking for a specific signal. Field names are device-specific; use
   them exactly as returned.
3. **Pick the cheapest tool that answers the question:**

| Question | Tool |
| - | - |
| "Current state of everything" / fleet snapshot | `telemetry_get_overview` (omit `device_ids` for the whole org) |
| Latest value of one signal | `telemetry_get_last` |
| Latest value of several signals on one device | `telemetry_get_multi_last` |
| History / trend of one signal | `telemetry_get_range` |
| History of several signals on one device | `telemetry_get_multi_range` |

## Limits

- Range queries cover at most **90 days**; `start_time` and `end_time` are
  required for the range tools.
- Batch calls take at most **20** `fields` or **20** `device_ids`. Split larger
  requests into several calls.
- For long windows, pass a coarser `window_seconds` (e.g. `3600` for hourly,
  `86400` for daily) instead of asking for raw points. Omitted, it auto-sizes
  to ~100 windows.
- `aggregation` / `aggregations` accepts `mean` (default), `max`, `min`,
  `last`, `first`, `sum`, `count`, `median`, `stddev`.

## Errors

- A device the caller can't access comes back in `errors` (overview) or as a
  tool error. Tell the user the token isn't scoped to that device rather than
  retrying.
- An authentication failure means the token is missing, expired, or revoked.
  Point the user to the plugin's setup instructions to set a new token.
