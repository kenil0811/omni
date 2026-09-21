#!/usr/bin/env bash
# Build the arm64 desktop .app, ad-hoc signed (no Apple Developer account; see
# docs/PLAN.md decision 7).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(cd "$HERE/../.." && pwd)"
TAURI_DIR="$APP_ROOT/apps/desktop/src-tauri"

if [[ ! -x "$TAURI_DIR/resources/python/bin/python3" ]]; then
  "$HERE/fetch_python.sh"
fi

# The bundler shells out to xattr/codesign/ditto. A developer PATH can shadow
# them (python.org installs put a pip `xattr` ahead of /usr/bin/xattr, which
# lacks -r and breaks bundling). Use Apple's tools, plus cargo.
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.cargo/bin"

cd "$TAURI_DIR"
cargo tauri build

APP="$TAURI_DIR/target/release/bundle/macos/Alpha.app"
echo
echo "built: $APP"
echo "size:  $(du -sh "$APP" | cut -f1)  (python: $(du -sh "$APP/Contents/Resources/python" | cut -f1))"
codesign --verify --deep --strict "$APP" && echo "codesign: valid (ad-hoc)"
