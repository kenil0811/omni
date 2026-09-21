# Build Brief — Work Tracker

## Outcome

A small tracker for pieces of work. I add items, change them as things move,
filter by status, and see a count of where everything stands. Two edits to the
same item shouldn't silently overwrite each other.

## Data

Store items in a table Resource called `items`. Each item has:

| Field | Type | Rule |
|---|---|---|
| `title` | string | required, non-empty |
| `status` | string | one of `todo`, `doing`, `done`; defaults to `todo` |
| `priority` | integer | 1–5; defaults to `3` |
| `notes` | string | optional, defaults to `""` |

Reject anything else with `app_sdk.InvalidInput` and a readable message.

## Entrypoints

Use exactly these ids, inputs, and output keys.

### `create_item` — kind `action`

Input: `{"title": "Draft the report", "status": "todo", "priority": 2}` —
`status`, `priority`, and `notes` are optional and take the defaults above.

Output: `{"id": "<id>", "revision": 1}`

### `update_item` — kind `action`

Input: `{"id": "<id>", "revision": 1, "changes": {"status": "doing"}}`

`revision` is the revision the caller last saw. If it no longer matches the
stored revision, the update must fail — let the SDK's `RevisionConflict`
propagate rather than overwriting. Validate `changes` by the same rules as
creation.

Output: `{"id": "<id>", "revision": 2}` — the new revision.

### `list_items` — kind `query`

Input: `{"status": "todo"}` or `{}` for everything.

Output: `{"items": [ ... ], "total": <int>}` — ordered by `priority` ascending
(1 first), then by `title`.

### `summarize` — kind `query`

Input: `{}`

Output:

```json
{"total": 5, "by_status": {"todo": 3, "doing": 1, "done": 1}}
```

`by_status` always has all three keys, using `0` when none are in that status.

## Notes

- `ctx.resources.table("items")` gives you `insert`, `get`, `list`, `all`,
  `update(id, changes, revision=...)`, and `delete`. Updating with a `revision`
  that no longer matches raises `RevisionConflict` for you.
- No custom UI. The platform renders the fallback from these Entrypoints.
- Keep it in `src/handlers.py` unless there's a reason to split.
