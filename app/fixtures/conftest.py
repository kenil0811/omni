"""Shared plumbing for the independent fixture oracles.

An oracle checks a *generated* App. The runner points it at one with
ALPHA_APP_DIR; without that the oracle skips, so a bare `pytest` stays green.
"""

from __future__ import annotations

import functools
import http.server
import os
import threading
from pathlib import Path

import pytest


@pytest.fixture
def app_dir() -> Path:
    """Directory of the generated App under test."""
    raw = os.environ.get("ALPHA_APP_DIR")
    if not raw:
        pytest.skip("set ALPHA_APP_DIR to the generated App to run this oracle")
    path = Path(raw).resolve()
    if not (path / "app.yaml").exists():
        pytest.fail(f"no app.yaml in {path}")
    return path


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args: object) -> None:  # keep test output readable
        pass


@pytest.fixture
def serve_dir():
    """Serve a directory over loopback HTTP; yields a url-builder.

    url = serve_dir(data_path)
    url("snapshot-1.json")  # -> http://127.0.0.1:<port>/snapshot-1.json
    """
    servers: list[http.server.ThreadingHTTPServer] = []

    def start(directory: Path):
        handler = functools.partial(_QuietHandler, directory=str(directory))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        servers.append(server)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        port = server.server_address[1]
        return lambda name: f"http://127.0.0.1:{port}/{name}"

    yield start
    for server in servers:
        server.shutdown()
        server.server_close()
