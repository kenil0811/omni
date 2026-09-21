# App SDK reference

The only route from App code to the platform. There is no other API: no
database connection, no credentials, no network client, no platform internals.

## Declaring an Entrypoint

```python
from app_sdk import entrypoint


@entrypoint("import_files", kind="action", description="Import selected CSV files")
def import_files(input: dict, ctx) -> dict:
    return {"imported": 0}
```

`kind` is `"action"` (does something), `"query"` (reads), or `"job"` (runs on a
schedule). The function takes `(input: dict, ctx: Context)` and returns a
JSON-serializable `dict`. Declare each Entrypoint in `app.yaml` too, with
`handler: "<module>.<function>"` resolved against `src/`.

One definition is enough: the platform builds the UI, the Assistant tool, and
the API from it.

## Context

| Member | What it gives you |
|---|---|
| `ctx.resources` | this App's tables and file stores |
| `ctx.artifacts` | immutable outputs and evidence |
| `ctx.config` | the user's configuration for this Release (a dict) |
| `ctx.log(message)` | a short progress line the user sees |
| `ctx.selected_files()` | `Path`s the user deliberately selected |
| `ctx.app_id`, `ctx.run_id`, `ctx.entrypoint_id` | identity of this execution |

## Tables

```python
table = ctx.resources.table("orders")

table.insert({"id": "A-1", "customer": "Rivera Ltd", "amount": 120.0})
table.upsert({"id": "A-1", "amount": 130.0})  # insert, or update if id exists
table.get("A-1")  # -> dict | None
table.all()  # -> list[dict], every record
table.all(where={"status": "paid"})  # exact-match filter
table.count(where={"status": "paid"})  # -> int
table.update("A-1", {"status": "paid"}, revision=1)
table.delete("A-1")

page = table.list(where={"status": "paid"}, limit=100, cursor=None)
page.records, page.cursor  # cursor is None on the last page
```

Every record carries `id`, `revision`, `created_at`, `updated_at`. Supply `id`
yourself when you have a natural key — that is what makes a repeated run
idempotent instead of creating duplicates. `revision` starts at 1 and rises by
one per update.

Passing `revision=` to `update` is an optimistic check: if the stored revision
has moved on, it raises `RevisionConflict` instead of overwriting. Omit it to
force the write.

Filters are exact matches on top-level fields. There is no aggregation, join, or
range query — read the records and compute in Python.

## Artifacts

```python
ref = ctx.artifacts.write("report.md", "# Summary\n\n7 imported", "text/markdown")
ctx.artifacts.write_json("results.json", {"imported": 7})
ctx.artifacts.read("report.md")  # -> bytes
```

`write` returns an `ArtifactRef`; `ref.name` is how the artifact is looked up
again. Return the name in your output so the user can open it.

## File stores

```python
files = ctx.resources.files("uploads")
files.put("invoice.pdf", data, "application/pdf")
files.get("invoice.pdf")  # -> bytes | None
files.list()  # -> list[str]
```

## Errors

```python
from app_sdk import InvalidInput, UnsupportedInput, ExternalUnavailable
```

| Raise | When |
|---|---|
| `InvalidInput` | the input cannot be processed — bad value, missing field, missing file |
| `UnsupportedInput` | a format this App does not handle; say what is supported |
| `ExternalUnavailable` | a required external route failed; retryable |

The message is shown to the user, so write it in plain language. Let
`RevisionConflict` propagate — the platform explains it.

## Testing

```python
from app_sdk.testing import harness


def test_it():
    with harness(APP_DIR) as app:  # APP_DIR = Path(__file__).parents[1]
        result = app.invoke("import_files", {"files": [...]})
        assert result["imported"] == 7
        assert app.table("orders").count() == 7
```

`harness` gives the App a disposable workspace with real SQLite and a real
Artifact store, then invokes Entrypoints exactly as the platform does. Pass
`config={...}` to set `ctx.config`. Use real data, not mocks.
