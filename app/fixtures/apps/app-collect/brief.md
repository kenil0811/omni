# Build Brief — Source Watch

## Outcome

I want to keep an eye on a product listing feed. Pull the listing from a URL I
give it, keep one record per item, and don't create duplicates when I run it
again. Some rows in the feed are junk — skip those but tell me why. Flag
anything above a price I set so I can spot expensive items.

## Configuration

| Key | Type | Default | Meaning |
|---|---|---|---|
| `watch_above` | number | `100` | A record whose `price` is strictly greater than this is flagged |

Read it from `ctx.config`.

## Data

The source URL returns JSON: an object with a `"rows"` array. Each row looks
like `{"ref": "A-1001", "title": "Cast iron skillet", "price": 39.5, "category": "kitchen"}`.

A row is **valid** only when all of these hold:

- `ref` is a non-empty string
- `title` is a non-empty string
- `price` is a number (int or float) and is not negative

Anything else is invalid: skip it and report the reason.

`ref` identifies the item. Two rows with the same `ref` are the same item — store
it once. Running collection again over a feed where an item's details changed
must **update** that item, not add a second one.

Store records in a table Resource called `records`, keyed by `ref` (use `ref` as
the record `id`). Each stored record must have: `ref`, `title`, `price`,
`category`, and `watched` (boolean, true when `price > watch_above`). Recompute
`watched` whenever the record is stored or updated.

## Entrypoints

Use exactly these ids, inputs, and output keys.

### `collect` — kind `job`

Input: `{"source_url": "<http url>"}`

Fetch that URL (the standard library is fine — `urllib.request`), parse the
rows, and store them.

Output:

```json
{
  "fetched": 12,
  "stored": 8,
  "updated": 0,
  "invalid": [{"ref": "A-1009", "reason": "title is empty"}]
}
```

- `fetched` — rows in the feed
- `stored` — records newly created this run
- `updated` — existing records changed this run
- `invalid` — one entry per rejected row, with `ref` (or `null` if unusable) and
  a short plain-language `reason`

### `list_records` — kind `query`

Input: `{"watched": true}`, `{"watched": false}`, or `{}` for everything.

Output: `{"records": [ ... ], "total": <int>}` — `records` is the stored
records, `total` is how many are in `records`.

## Notes

- No browser, no site-specific logic. It's a plain HTTP GET.
- A network failure should raise `app_sdk.ExternalUnavailable` with a readable message.
- Keep it in `src/handlers.py` unless there's a reason to split.
