"""Immutable outputs and evidence, addressed by content digest."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtifactRef:
    """A handle to immutable bytes. Generated code never sees a filesystem path."""

    name: str
    digest: str
    media_type: str
    size_bytes: int

    def __str__(self) -> str:  # so it can be placed straight into outputs
        return self.digest


class Artifacts:
    def __init__(self, root: Path) -> None:
        self._root = Path(root)
        (self._root / "blobs").mkdir(parents=True, exist_ok=True)
        self._index = self._root / "index.json"
        if not self._index.exists():
            self._index.write_text("{}", encoding="utf-8")

    def _blob_path(self, digest: str) -> Path:
        return self._root / "blobs" / digest

    def write(self, name: str, content: bytes | str, media_type: str = "text/plain") -> ArtifactRef:
        """Store bytes and return a reference. Writing identical bytes is a no-op."""
        raw = content.encode("utf-8") if isinstance(content, str) else bytes(content)
        digest = hashlib.sha256(raw).hexdigest()
        blob = self._blob_path(digest)
        if not blob.exists():
            tmp = blob.with_suffix(".tmp")
            tmp.write_bytes(raw)
            tmp.replace(blob)
        index = json.loads(self._index.read_text(encoding="utf-8"))
        index[name] = {
            "digest": digest,
            "media_type": media_type,
            "size_bytes": len(raw),
        }
        self._index.write_text(json.dumps(index, indent=2, sort_keys=True), encoding="utf-8")
        return ArtifactRef(name=name, digest=digest, media_type=media_type, size_bytes=len(raw))

    def write_json(self, name: str, value: object) -> ArtifactRef:
        return self.write(
            name, json.dumps(value, indent=2, sort_keys=True, default=str), "application/json"
        )

    def read_digest(self, digest: str) -> bytes:
        blob = self._blob_path(digest)
        if not blob.exists():
            raise FileNotFoundError(f"artifact bytes missing for digest {digest}")
        return blob.read_bytes()

    def read(self, name: str) -> bytes:
        index = json.loads(self._index.read_text(encoding="utf-8"))
        if name not in index:
            raise FileNotFoundError(f"no artifact named {name!r}")
        return self.read_digest(index[name]["digest"])

    def names(self) -> list[str]:
        return sorted(json.loads(self._index.read_text(encoding="utf-8")))
