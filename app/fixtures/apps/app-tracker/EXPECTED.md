# app-tracker — expected results

Written before any App was generated. The oracle asserts these.

## Seed used by the oracle

| Title | Status | Priority |
|---|---|---|
| Draft the report | `todo` | 2 |
| Call the supplier | `doing` | 1 |
| File expenses | `todo` | 4 |
| Book travel | `done` | 3 |
| Review contract | `todo` | 1 |

Created with defaults where a field is omitted: `status` → `todo`,
`priority` → `3`, `notes` → `""`.

## Expected

| Check | Expected |
|---|---|
| New item revision | `1` |
| `list_items {}` total | 5 |
| `list_items {"status": "todo"}` total | 3 |
| `summarize` | `{"total": 5, "by_status": {"todo": 3, "doing": 1, "done": 1}}` |
| Order of `list_items {}` | `Call the supplier` (1), `Review contract` (1), `Draft the report` (2), `Book travel` (3), `File expenses` (4) |

Priority ties break on title, so `Call the supplier` precedes `Review contract`.

## Optimistic revision

1. Create an item → revision `1`.
2. Update with `revision: 1` → succeeds, returns revision `2`.
3. Update again with `revision: 1` → **must raise `RevisionConflict`**, and the
   stored item must still hold the value written in step 2.

## Validation

Each of these must raise `InvalidInput`, and must not create or change a record:

- empty `title` on create
- `status: "archived"` on create or update
- `priority: 0` or `priority: 9`

An empty `by_status` bucket is `0`, never a missing key: with only `todo` items,
`summarize` still returns `doing` and `done` as `0`.
