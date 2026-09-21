# app-files — expected results

Derived from the fixture CSVs by hand, before any App was generated. The oracle
asserts these. A mismatch is a failed run, never a reason to edit this file.

## Importing both files

`orders-a.csv` — 5 rows, all valid.
`orders-b.csv` — 4 rows, 2 valid:

| Line | Row | Verdict |
|---|---|---|
| 2 | `B-1` 210.00 paid | valid |
| 3 | `B-2` amount empty | **exception** — amount is not a number |
| 4 | `B-3` status `shipped` | **exception** — status not one of new/paid/cancelled |
| 5 | `B-4` 18.75 new | valid |

| | |
|---|---|
| **Imported** | **7** — `A-1`…`A-5`, `B-1`, `B-4` |
| **Exceptions** | **2** — `orders-b.csv` lines 3 and 4 |

Status counts over the 7 imported:

| Status | Count | Orders |
|---|---|---|
| `paid` | 3 | `A-1`, `A-3`, `B-1` |
| `new` | 3 | `A-2`, `A-5`, `B-4` |
| `cancelled` | 1 | `A-4` |

Amount total: 876.49.

## Importing `orders-a.csv` alone

5 imported, 0 exceptions. `paid` 2, `new` 2, `cancelled` 1.
