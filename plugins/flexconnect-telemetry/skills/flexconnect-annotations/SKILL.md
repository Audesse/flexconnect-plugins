---
name: flexconnect-annotations
description: Record, find, and remove timestamped annotations on Flexconnect devices (e.g. "mark the start of a new experiment", "what experiments ran on device 12 last month?", "delete that note") using the Flexconnect telemetry MCP tools. Use when the user wants to note an event on a device's timeline, look up past notes, or line readings up against those notes.
---

# Flexconnect device annotations

An annotation is a short note (1–128 characters) pinned to one device at one
UTC instant. It's usually the start of an experiment, a configuration change,
or a test run. Annotations sit alongside the device's readings, so a reading
trend can be read against "what was going on at the time".

All timestamps are ISO-8601 UTC (`2024-04-01T09:30:00Z`).

## Tools

| Tool | Does | Needs |
| - | - | - |
| `telemetry_list_annotations` | Annotations for one device in a time range, oldest first | normal telemetry access |
| `telemetry_create_annotation` | Adds one annotation (at `timestamp`, or now if omitted) and returns it with its `annotation_id` | write permission on the token |
| `telemetry_delete_annotation` | Permanently removes one annotation by `annotation_id` | write permission on the token |

Creating and deleting **change shared data** that the user's whole org sees
(dashboards included). Listing is read-only.

## Workflow

1. **Resolve the device.** Map the alias the user mentions to a `device_id`
   with `telemetry_list_devices`. An 8-character short code also works
   wherever a `device_id` is taken. Don't guess ids.
2. **Pin down the timestamp before creating.** `timestamp` is optional.
   - "Now" or "just started": omit `timestamp`, and the server stamps the
     annotation with its own current UTC time. This is more accurate than
     the agent's own clock.
   - A local time ("9:30 this morning"): convert it to UTC. If you don't know
     the user's timezone, ask instead of assuming.
   - A vague time ("sometime yesterday afternoon"): ask for the exact time.
     An annotation at the wrong instant is worse than none.
3. **Keep the text within 128 characters.** Write a concise, specific label,
   such as `Experiment 7 start: new tire set, 95 psi cold`. If the user's
   wording is longer, shorten it and show them the result. Don't silently
   truncate mid-word.
4. **Confirm writes when they're ambiguous.** If the user clearly asked for
   this exact annotation, just create it. Otherwise (you inferred the text or
   time, or it's one of several devices), state the device, the UTC time and
   the text, and ask first.
5. **Report the result.** After creating, give the device, the UTC time (as
   returned, which matters when you omitted it), the text and the returned
   `annotation_id`. The user needs that id to delete
   the annotation later.

## Finding annotations

- `telemetry_list_annotations` needs `start_time` and `end_time`, and the
  range can be at most **90 days**.
- Results come back oldest first, **up to 100 per call**. When the response
  has a non-null `next_cursor`, call again with the **same** `device_id`,
  `start_time` and `end_time` plus `cursor=<next_cursor>`, and repeat until
  `next_cursor` is null. Don't change the range between pages: a cursor is
  only valid for the range that produced it. If the user only needs the
  latest few, narrow the range instead of paging through everything.
- For "all experiments this year", walk back in consecutive 90-day windows
  (paging within each) and merge the results. Stop once a few
  windows come back empty, unless the user wants the full history.
- To compare readings across experiments, list the annotations first. Then
  use each annotation's timestamp as a boundary for `telemetry_get_range` or
  `telemetry_get_multi_range`: from one experiment's start to the next one's
  start, or to now for the last one.
- Annotations belong to one device. For a fleet-wide question, list per
  device.

## Deleting

- Deletion is **permanent**. You need the `annotation_id`, so list first to
  find it.
- Before deleting, show the user the matching annotation (time and text) and
  confirm, unless they already named the exact id. Never bulk-delete
  ("clear all annotations") without listing what would go and getting an
  explicit yes.
- A "not found" error means it's already gone or belongs to another
  device. Say so, and don't retry.

## Errors

- **Permission error on create or delete:** the connection can read
  telemetry but isn't allowed to write annotations. Don't retry. Tell the
  user why, which is one of two things:
  - **Signed in through the browser:** the app only gets annotation writes
    if it asked for them when connecting and the pasted key allows them.
    They'll need to reconnect with write access.
  - **Using a key directly:** the key itself needs the device-metadata
    write permission. A Flexconnect org admin can issue one.
- **Validation error:** the text is empty or longer than 128 characters, the
  timestamp isn't valid ISO-8601 with a timezone, or the list range exceeds
  90 days. Fix the input and try again once.
- **Device not accessible:** the token isn't scoped to that device. Tell the
  user rather than trying other ids.
