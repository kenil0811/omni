"""EXP-PACKAGE stand-in for the Python platform service.

Speaks line-delimited JSON on stdin/stdout. The real Core replaces this in plan
step 3; this file only answers "does the bundled interpreter work from inside
the .app with nothing else installed?".
"""

from __future__ import annotations

import json
import os
import sqlite3
import ssl
import sys
import time
import urllib.request

STARTED = time.monotonic()


def _sqlite_json() -> str:
    conn = sqlite3.connect(":memory:")
    try:
        return str(conn.execute("""SELECT json_extract('{"a": 7}', '$.a')""").fetchone()[0])
    finally:
        conn.close()


def _https() -> dict:
    """Can the bundled interpreter verify a real TLS certificate?"""
    stats = ssl.create_default_context().cert_store_stats()
    result = {
        "ca_certs_loaded": stats.get("x509_ca", 0),
        "paths": ssl.get_default_verify_paths()._asdict(),
    }
    try:
        with urllib.request.urlopen("https://www.python.org/", timeout=10) as response:
            result["get_python_org"] = f"ok {response.status}"
    except Exception as exc:  # noqa: BLE001 - reported, not raised
        result["get_python_org"] = f"{type(exc).__name__}: {exc}"[:300]
    return result


def ping() -> dict:
    return {
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "prefix": sys.prefix,
        "inside_app_bundle": ".app/Contents/" in sys.executable,
        "isolated_flag": bool(sys.flags.isolated),
        "dont_write_bytecode": bool(sys.dont_write_bytecode),
        "sqlite": sqlite3.sqlite_version,
        "sqlite_json_extract": _sqlite_json(),
        "openssl": ssl.OPENSSL_VERSION,
        "https": _https(),
        "path_env": os.environ.get("PATH", "<unset>"),
        "pid": os.getpid(),
        "uptime_ms": round((time.monotonic() - STARTED) * 1000),
    }


def main() -> None:
    print(json.dumps({"ready": True, "pid": os.getpid()}), flush=True)
    for line in sys.stdin:
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            print(json.dumps({"error": "invalid json"}), flush=True)
            continue
        if request.get("op") == "ping":
            print(json.dumps(ping()), flush=True)
        elif request.get("op") == "shutdown":
            print(json.dumps({"bye": True}), flush=True)
            return
        else:
            print(json.dumps({"error": f"unknown op {request.get('op')!r}"}), flush=True)


if __name__ == "__main__":
    main()
