# app-collect — expected results

Derived from the fixture data by hand, before any App was generated. The oracle
asserts these. Never change them to match generated output; a mismatch is a
failed run.

## Snapshot 1 (12 rows)

| | |
|---|---|
| Rows in feed | 12 |
| Distinct valid items | 8 (`A-1001`…`A-1008`) |
| Duplicate rows | 2 (second `A-1003`, second `A-1006`) |
| Invalid rows | 2 (`A-1009` empty title, `A-1010` non-numeric price) |
| **Records stored** | **8** |
| Updated | 0 |
| Watched (`price > 100`) | 3 — `A-1002` 289.0, `A-1004` 120.0, `A-1005` 210.0 |

Re-running collection over snapshot 1 must still leave 8 records, 0 stored, 0 updated.

## Snapshot 2 (10 rows)

Adds `A-1011` (150.0) and `A-1012` (32.0); changes `A-1006` from 95.0 to 130.0.

| | |
|---|---|
| Rows in feed | 10 |
| **Records after** | **10** |
| Newly stored | 2 (`A-1011`, `A-1012`) |
| Updated | 1 (`A-1006`) |
| Watched | 5 — `A-1002`, `A-1004`, `A-1005`, `A-1006` (now 130.0), `A-1011` |

No duplicate is created for any `ref` present in both snapshots.

## With `watch_above = 200`

Snapshot 1 watched: 2 — `A-1002` 289.0, `A-1005` 210.0.
