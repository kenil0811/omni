# Build Brief — Order Intake

## Outcome

I get order exports as CSV files. I want to drop a few in, have the good rows
pulled into one place I can filter, see exactly which rows were rejected and
why, and get a short summary I can save.

## Data

Each CSV has a header row: `order_id,customer,amount,status`.

A row is **valid** only when all of these hold:

- `order_id` is non-empty
- `customer` is non-empty
- `amount` parses as a number and is not negative
- `status` is one of `new`, `paid`, `cancelled`

Anything else is an exception: don't import it, and record why.

Store valid rows in a table Resource called `orders`, keyed by `order_id` (use it
as the record `id`), with `order_id`, `customer`, `amount` (number), `status`,
and `source_file` (the file's name, not its full path).

If the same `order_id` appears twice, the first one wins and the later one is an
exception.

## Entrypoints

Use exactly these ids, inputs, and output keys.

### `import_files` — kind `action`

Input: `{"files": ["/abs/path/a.csv", "/abs/path/b.csv"]}`

Read each file, import the valid rows, and write a summary report Artifact.

Output:

```json
{
  "imported": 7,
  "exceptions": [{"file": "orders-b.csv", "row": 3, "reason": "amount is empty"}],
  "report": "<artifact name you wrote>"
}
```

- `imported` — rows stored this call
- `exceptions` — one entry per rejected row: `file` (name only), `row` (1-based
  line number in the file, where the header is line 1, so the first data row is
  2), and a short plain-language `reason`
- `report` — the name you passed to `ctx.artifacts.write(...)`

The report is Markdown. It must state the number imported, the number of
exceptions, and a count per status. Keep it short; a person reads it.

A file that does not exist, or is not a readable CSV, should raise
`app_sdk.InvalidInput` naming the file.

### `list_orders` — kind `query`

Input: `{"status": "paid"}` or `{}` for everything.

Output: `{"orders": [ ... ], "total": <int>}`.

## Notes

- `csv` from the standard library is fine. No external dependencies needed.
- Keep it in `src/handlers.py` unless there's a reason to split.
