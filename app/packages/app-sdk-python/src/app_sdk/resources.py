"""App-scoped Resources: tables with optimistic revisions, and file stores.

Mirrors decision D-041: create/get/list/update/delete, optimistic revision
checks, declared exact-match filters, stable cursor pagination, and
Artifact-backed file namespaces. No aggregation, no reference expansion, no
migration framework.
"""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ResourceError(RuntimeError):
    """Base class for Resource failures surfaced to generated code."""


class RecordNotFound(ResourceError):
    pass


class RevisionConflict(ResourceError):
    """Raised when an update targets a stale revision."""


@dataclass
class Page:
    records: list[dict[str, Any]]
    cursor: str | None


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class Table:
    """One App-scoped table. Records are JSON objects with id and revision."""

    def __init__(self, conn: sqlite3.Connection, name: str) -> None:
        self._conn = conn
        self._name = name
        self._table = f"resource_{name}"
        self._conn.execute(
            f"""CREATE TABLE IF NOT EXISTS "{self._table}" (
                id TEXT PRIMARY KEY,
                revision INTEGER NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )"""
        )
        self._conn.commit()

    @staticmethod
    def _row(row: sqlite3.Row) -> dict[str, Any]:
        record = json.loads(row["data"])
        record["id"] = row["id"]
        record["revision"] = row["revision"]
        record["created_at"] = row["created_at"]
        record["updated_at"] = row["updated_at"]
        return record

    def insert(self, record: dict[str, Any]) -> dict[str, Any]:
        """Insert a record. Supply `id` for a stable key, or one is generated."""
        data = dict(record)
        record_id = str(data.pop("id", None) or uuid.uuid4())
        for reserved in ("revision", "created_at", "updated_at"):
            data.pop(reserved, None)
        now = _now()
        try:
            self._conn.execute(
                f'INSERT INTO "{self._table}" (id, revision, data, created_at, updated_at)'
                " VALUES (?, 1, ?, ?, ?)",
                (record_id, json.dumps(data, sort_keys=True), now, now),
            )
        except sqlite3.IntegrityError as exc:
            raise ResourceError(f"record {record_id!r} already exists") from exc
        self._conn.commit()
        return self.get(record_id)

    def upsert(self, record: dict[str, Any]) -> dict[str, Any]:
        """Insert, or update in place when `id` already exists.

        Use this for idempotent collection so a repeated Run does not create
        duplicates.
        """
        record_id = record.get("id")
        if record_id is not None and self.get(str(record_id)) is not None:
            existing = self.get(str(record_id))
            changes = {
                k: v
                for k, v in record.items()
                if k not in ("id", "revision", "created_at", "updated_at")
            }
            return self.update(str(record_id), changes, revision=existing["revision"])
        return self.insert(record)

    def get(self, record_id: str) -> dict[str, Any] | None:
        row = self._conn.execute(
            f'SELECT * FROM "{self._table}" WHERE id = ?', (str(record_id),)
        ).fetchone()
        return self._row(row) if row else None

    def list(
        self,
        where: dict[str, Any] | None = None,
        limit: int = 100,
        cursor: str | None = None,
    ) -> Page:
        """List records, optionally filtered by exact match on top-level fields.

        Ordered by id for a stable cursor.
        """
        limit = max(1, min(int(limit), 1000))
        sql = f'SELECT * FROM "{self._table}"'
        params: list[Any] = []
        clauses: list[str] = []
        if cursor:
            clauses.append("id > ?")
            params.append(cursor)
        for key, value in (where or {}).items():
            clauses.append("json_extract(data, ?) = ?")
            params.extend([f"$.{key}", value])
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY id LIMIT ?"
        params.append(limit + 1)
        rows = self._conn.execute(sql, params).fetchall()
        records = [self._row(r) for r in rows[:limit]]
        next_cursor = records[-1]["id"] if len(rows) > limit and records else None
        return Page(records=records, cursor=next_cursor)

    def all(self, where: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Every matching record, following cursors. Convenience for small tables."""
        out: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            page = self.list(where=where, limit=500, cursor=cursor)
            out.extend(page.records)
            if not page.cursor:
                return out
            cursor = page.cursor

    def count(self, where: dict[str, Any] | None = None) -> int:
        return len(self.all(where=where))

    def update(
        self, record_id: str, changes: dict[str, Any], revision: int | None = None
    ) -> dict[str, Any]:
        """Merge `changes` into a record.

        When `revision` is given it must match the stored revision, otherwise
        RevisionConflict is raised.
        """
        current = self.get(record_id)
        if current is None:
            raise RecordNotFound(f"no record {record_id!r}")
        if revision is not None and int(revision) != current["revision"]:
            raise RevisionConflict(
                f"record {record_id!r} is at revision {current['revision']},"
                f" update supplied {revision}"
            )
        data = {
            k: v
            for k, v in current.items()
            if k not in ("id", "revision", "created_at", "updated_at")
        }
        for key, value in changes.items():
            if key not in ("id", "revision", "created_at", "updated_at"):
                data[key] = value
        self._conn.execute(
            f'UPDATE "{self._table}" SET data = ?, revision = revision + 1, updated_at = ?'
            " WHERE id = ?",
            (json.dumps(data, sort_keys=True), _now(), str(record_id)),
        )
        self._conn.commit()
        return self.get(record_id)

    def delete(self, record_id: str, revision: int | None = None) -> None:
        current = self.get(record_id)
        if current is None:
            raise RecordNotFound(f"no record {record_id!r}")
        if revision is not None and int(revision) != current["revision"]:
            raise RevisionConflict(f"record {record_id!r} revision mismatch")
        self._conn.execute(f'DELETE FROM "{self._table}" WHERE id = ?', (str(record_id),))
        self._conn.commit()


class FileStore:
    """A named file namespace backed by immutable Artifact bytes."""

    def __init__(self, conn: sqlite3.Connection, name: str, artifacts: Any) -> None:
        self._table = Table(conn, f"files_{name}")
        self._artifacts = artifacts

    def put(
        self, path: str, content: bytes | str, media_type: str = "application/octet-stream"
    ) -> dict[str, Any]:
        ref = self._artifacts.write(path, content, media_type)
        return self._table.upsert({"id": path, "artifact": ref.digest, "media_type": media_type})

    def get(self, path: str) -> bytes | None:
        entry = self._table.get(path)
        if entry is None:
            return None
        return self._artifacts.read_digest(entry["artifact"])

    def list(self) -> list[str]:
        return [r["id"] for r in self._table.all()]


class Resources:
    """Entry point to this App's own tables and file stores."""

    def __init__(self, db_path: Path, artifacts: Any) -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._artifacts = artifacts
        self._tables: dict[str, Table] = {}
        self._files: dict[str, FileStore] = {}

    def table(self, name: str) -> Table:
        if name not in self._tables:
            self._tables[name] = Table(self._conn, name)
        return self._tables[name]

    def files(self, name: str) -> FileStore:
        if name not in self._files:
            self._files[name] = FileStore(self._conn, name, self._artifacts)
        return self._files[name]

    def close(self) -> None:
        self._conn.close()
