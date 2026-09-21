# EXP-PACKAGE — can we ship Python inside a Tauri app with nothing else installed?

Status: **done — go**
Plan step: 2

## Question

Can the Tauri host launch a bundled, pinned CPython from inside the `.app`, talk
to it, and show the answer in the WebView — on a Mac where the app gets no PATH,
no HOME, and no developer tools — ad-hoc signed, without an Apple Developer
account?

## Built

| Path | What |
|---|---|
| `app/packaging/macos/fetch_python.sh` | Downloads pinned CPython 3.13.15 (python-build-standalone `20260901`, aarch64, `install_only_stripped`), verifies it against the **SHA-256 upstream publishes in the release's `SHA256SUMS`**, prunes GUI/dev files, precompiles the stdlib |
| `app/packaging/macos/build_app.sh` | Stages Python if needed, builds the `.app` with a clean PATH, verifies the signature |
| `app/apps/desktop/src-tauri/` | Rust host: spawns `python3 -I -B core.py` with an empty environment in its own process group, one command `ping_core`, `--selftest <file>` mode, shutdown on exit |
| `app/apps/desktop/dist/` | Static page that calls through to Python and shows the result |
| `app/apps/desktop/core_stub/core.py` | Stand-in for Core: JSON lines over stdin/stdout. Replaced in step 3 |

Build: `app/packaging/macos/build_app.sh` (19 s after first compile).

## Results

macOS 26.6.2, arm64, Rust 1.98.1, tauri-cli 2.11.5, CPython 3.13.15.

| Check | Result |
|---|---|
| `.app` size | **80 MB** — 73 MB Python, ~7 MB host + WebView shell |
| Signature | ad-hoc, `codesign --verify --deep --strict` valid |
| Launch with `env -i` (no PATH, no HOME) | pass — interpreter ran from `Alpha.app/Contents/Resources/python/bin/python3`, isolated mode on |
| Full path WebView → Rust → Python → rendered on page | pass, 6/6 launches (1 direct, 5 via LaunchServices `open`) |
| Python ready after launch | **253–336 ms** (LaunchServices runs: 253, 259, 263, 272, 276) |
| Page showing Python's answer after launch | **433–537 ms** |
| Idle memory | host 100 MB RSS, Python 30 MB RSS (WebKit helper processes not counted) |
| SQLite in bundled Python | 3.53.1, `json_extract` works (the SDK needs it) |
| HTTPS from bundled Python | pass — 128 CA certs from macOS `/etc/ssl/cert.pem`, real GET to python.org returned 200 |
| Host killed with `SIGKILL` | Python exited within 100 ms (reads EOF on its stdin) — no orphan |
| Normal quit (AppleScript `quit`) | host and Python both gone |
| Runtime writes into the signed bundle | none — only the main binary is newer than the signature seal, which is how `codesign` works |
| Downloaded (quarantined) copy | `spctl` rejects it, as it does any ad-hoc app. **The founder opened a downloaded copy and it worked** — see below |

## Problems found and fixed

1. **Tauri copies resources by following symlinks.** `python`, `python3` and
   `python3.13` became three identical 17 MB files. Staging now keeps one real
   binary named `python3` and fails if any symlink remains.
2. **A developer PATH broke bundling.** The python.org Python 3.11 install on
   this Mac puts a pip-installed `xattr` ahead of `/usr/bin/xattr`; it lacks
   `-r`, so Tauri's bundler failed. `build_app.sh` now builds with Apple's tools
   first on PATH. The user's install is untouched.
3. Precompiling the stdlib at packaging time is required, not optional: the
   bundle is signed and read-only, so Python must run with `-B` and never write
   `__pycache__` into it.

## First open of a downloaded copy (manual)

**Result (21 Sep 2026):** the founder downloaded a copy, opened it, and the app
worked ("able to see the app fine"). Whether macOS showed one prompt or two
was not recorded; the procedure is kept below for re-checking.

Needs a person to click through a macOS security prompt.

1. Zip `Alpha.app`, AirDrop or email it to yourself (or download it through a
   browser) so it carries the quarantine flag, and unzip it.
2. Double-click it. Expect: "Apple could not verify Alpha…".
3. System Settings → Privacy & Security → **Open Anyway**.
4. Record: does the window show "Platform service running: Python 3.13.15", or
   does macOS block the bundled `python3` separately? The interpreter carries its
   own quarantine flag, so a second prompt is possible.

If Python is blocked separately, the fix is to clear quarantine on the bundle's
contents at first launch or ship as a `.dmg`; both are small. It does not
change the go decision.

## Decision

**Go.** Python ships inside the app, runs with nothing installed, starts in about
a quarter second, and dies with its host. Nothing here needs an Apple Developer
account.

## Limitations

- arm64 only. x86_64 is plan step 8.
- `/etc/ssl/cert.pem` does not include certificates added to the Keychain (for
  example a company proxy's root). Users behind such a proxy would fail HTTPS;
  fix later with a Keychain-backed trust store (`truststore`) if it matters.
- Stdin/stdout is the spike's transport. Step 3 replaces it with loopback HTTP +
  token, per the plan.
- One machine. The machine has developer tools installed; `env -i` and
  LaunchServices launches show the app does not use them, but a clean second
  Mac or user account would be stronger evidence.
