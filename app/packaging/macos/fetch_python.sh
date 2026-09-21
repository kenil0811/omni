#!/usr/bin/env bash
# Stage the pinned relocatable CPython that the desktop app bundles.
#
# Source: python-build-standalone, install_only_stripped, aarch64-apple-darwin.
# The hash is the one upstream publishes in the release's SHA256SUMS; a mismatch
# stops the build. Output goes to apps/desktop/src-tauri/resources/python
# (gitignored — it is reproducible from this script).
set -euo pipefail

PBS_RELEASE="20260901"
PY_VERSION="3.13.15"
ARCHIVE="cpython-${PY_VERSION}+${PBS_RELEASE}-aarch64-apple-darwin-install_only_stripped.tar.gz"
URL="https://github.com/astral-sh/python-build-standalone/releases/download/${PBS_RELEASE}/${ARCHIVE//+/%2B}"
SHA256="d3904bd6a072246e07aa0bdadee9a14e80521e42a943c0848059feb16a2816dc"

HERE="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(cd "$HERE/../.." && pwd)"
DEST="$APP_ROOT/apps/desktop/src-tauri/resources/python"
CACHE="${XDG_CACHE_HOME:-$HOME/Library/Caches}/alpha-packaging"

if [[ "$(uname -m)" != "arm64" ]]; then
  echo "only arm64 is staged for now (plan step 2); this machine is $(uname -m)" >&2
  exit 1
fi

mkdir -p "$CACHE"
if [[ ! -f "$CACHE/$ARCHIVE" ]]; then
  echo "downloading $ARCHIVE"
  curl -fsSL -o "$CACHE/$ARCHIVE.part" "$URL"
  mv "$CACHE/$ARCHIVE.part" "$CACHE/$ARCHIVE"
fi
echo "$SHA256  $CACHE/$ARCHIVE" | shasum -a 256 -c -

rm -rf "$DEST"
mkdir -p "$DEST"
tar -xzf "$CACHE/$ARCHIVE" -C "$DEST" --strip-components=1

before=$(du -sk "$DEST" | cut -f1)

# Drop what a headless platform service never uses. Nothing here is imported by
# Core or by generated Apps; tkinter needs a display, idle/turtle are GUIs.
rm -rf "$DEST"/include "$DEST"/share \
       "$DEST"/lib/tcl* "$DEST"/lib/tk* "$DEST"/lib/itcl* "$DEST"/lib/thread* \
       "$DEST"/lib/python3.13/{idlelib,tkinter,turtledemo,turtle.py} \
       "$DEST"/lib/python3.13/lib-dynload/_tkinter*.so \
       "$DEST"/bin/idle* "$DEST"/bin/pydoc* \
       "$DEST"/bin/pip* "$DEST"/bin/*-config "$DEST"/lib/pkgconfig

# Tauri dereferences symlinks when it copies resources, which would put three
# identical 17 MB interpreters in the bundle. Keep one real binary, named
# python3 (what the host launches); the name does not affect stdlib lookup.
rm -f "$DEST/bin/python" "$DEST/bin/python3"
mv "$DEST/bin/python3.13" "$DEST/bin/python3"
if find "$DEST" -type l | grep -q .; then
  echo "unexpected symlinks remain; they would be duplicated in the bundle:" >&2
  find "$DEST" -type l >&2
  exit 1
fi

# The app bundle is signed and read-only, so Python must never write
# __pycache__ into it at runtime. Compile the stdlib now instead; this also
# keeps cold start fast.
"$DEST/bin/python3" -I -m compileall -q -j 0 "$DEST/lib/python3.13" >/dev/null || true

after=$(du -sk "$DEST" | cut -f1)
echo "staged CPython $PY_VERSION ($PBS_RELEASE) at $DEST"
echo "size: ${before} KiB extracted -> ${after} KiB after pruning + bytecode"
"$DEST/bin/python3" -I -c 'import sys, sqlite3, ssl; print(sys.version.split()[0], "sqlite", sqlite3.sqlite_version, ssl.OPENSSL_VERSION)'
