//! Alpha desktop host — EXP-PACKAGE spike (plan step 2).
//!
//! Starts the bundled CPython from inside the .app, talks to it over a pipe, and
//! exposes one command to the trusted page. `--selftest <file>` loads the page,
//! lets it call through to Python, writes what it rendered to <file>, and quits;
//! that makes the whole WebView -> Rust -> Python path checkable without a person.

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::io::{BufRead, BufReader, Write};
use std::os::unix::process::CommandExt;
use std::path::{Path, PathBuf};
use std::process::{Child, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::Mutex;
use std::time::{Duration, Instant};

use serde_json::{json, Value};
use tauri::{Manager, RunEvent};

const SELFTEST_TIMEOUT: Duration = Duration::from_secs(30);

struct Core {
    child: Child,
    stdin: ChildStdin,
    stdout: BufReader<ChildStdout>,
}

impl Core {
    fn request(&mut self, message: &Value) -> Result<Value, String> {
        writeln!(self.stdin, "{message}").map_err(|e| format!("write to core: {e}"))?;
        self.stdin.flush().map_err(|e| format!("flush to core: {e}"))?;
        let mut line = String::new();
        let read = self
            .stdout
            .read_line(&mut line)
            .map_err(|e| format!("read from core: {e}"))?;
        if read == 0 {
            return Err("core closed its output (it exited)".into());
        }
        serde_json::from_str(&line).map_err(|e| format!("core sent invalid json: {e}"))
    }

    /// Ask politely, then insist. Returns how it ended, for the record.
    fn shutdown(mut self) -> &'static str {
        let _ = self.request(&json!({ "op": "shutdown" }));
        let deadline = Instant::now() + Duration::from_secs(2);
        while Instant::now() < deadline {
            if let Ok(Some(_)) = self.child.try_wait() {
                return "exited";
            }
            std::thread::sleep(Duration::from_millis(20));
        }
        // Kill the whole process group so nothing the core started survives.
        let pid = self.child.id() as i32;
        let _ = Command::new("/bin/kill").args(["-KILL", &format!("-{pid}")]).status();
        let _ = self.child.wait();
        "killed"
    }
}

struct AppState {
    core: Mutex<Option<Core>>,
    launched: Instant,
    core_ready_ms: Mutex<Option<u128>>,
    core_error: Mutex<Option<String>>,
    selftest_out: Option<PathBuf>,
}

fn spawn_core(resources: &Path) -> Result<Core, String> {
    let python = resources.join("python/bin/python3");
    let script = resources.join("core/core.py");
    for required in [&python, &script] {
        if !required.exists() {
            return Err(format!("missing bundled file: {}", required.display()));
        }
    }
    let mut command = Command::new(&python);
    // -I: ignore PYTHON* variables and user site-packages.
    // -B: never write __pycache__ into the signed, read-only bundle.
    command
        .args(["-I", "-B"])
        .arg(&script)
        .env_clear()
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::inherit())
        .process_group(0);
    if let Some(home) = std::env::var_os("HOME") {
        command.env("HOME", home);
    }
    let mut child = command
        .spawn()
        .map_err(|e| format!("could not start {}: {e}", python.display()))?;
    let stdin = child.stdin.take().ok_or("no stdin")?;
    let stdout = BufReader::new(child.stdout.take().ok_or("no stdout")?);
    let mut core = Core { child, stdin, stdout };

    let mut line = String::new();
    core.stdout
        .read_line(&mut line)
        .map_err(|e| format!("waiting for core: {e}"))?;
    let hello: Value =
        serde_json::from_str(&line).map_err(|_| format!("core did not start: {line:?}"))?;
    if hello["ready"] != json!(true) {
        return Err(format!("core did not report ready: {hello}"));
    }
    Ok(core)
}

#[tauri::command]
fn ping_core(state: tauri::State<'_, AppState>) -> Result<Value, String> {
    if let Some(error) = state.core_error.lock().unwrap().clone() {
        return Err(error);
    }
    let mut guard = state.core.lock().unwrap();
    let core = guard.as_mut().ok_or("core is not running")?;
    let started = Instant::now();
    let mut reply = core.request(&json!({ "op": "ping" }))?;
    reply["roundtrip_ms"] = json!(started.elapsed().as_millis());
    reply["core_ready_ms"] = json!(*state.core_ready_ms.lock().unwrap());
    Ok(reply)
}

#[tauri::command]
fn report_ui(
    app: tauri::AppHandle,
    state: tauri::State<'_, AppState>,
    result: Value,
    rendered: String,
) -> Result<(), String> {
    let Some(path) = &state.selftest_out else {
        return Ok(());
    };
    let report = json!({
        "via_webview": true,
        "rendered": rendered,
        "result": result,
        "launch_to_report_ms": state.launched.elapsed().as_millis(),
    });
    std::fs::write(path, serde_json::to_vec_pretty(&report).unwrap())
        .map_err(|e| format!("could not write selftest report: {e}"))?;
    app.exit(0);
    Ok(())
}

fn selftest_path() -> Option<PathBuf> {
    let args: Vec<String> = std::env::args().collect();
    args.iter()
        .position(|a| a == "--selftest")
        .and_then(|i| args.get(i + 1))
        .map(PathBuf::from)
}

fn main() {
    let launched = Instant::now();
    let selftest_out = selftest_path();

    let app = tauri::Builder::default()
        .manage(AppState {
            core: Mutex::new(None),
            launched,
            core_ready_ms: Mutex::new(None),
            core_error: Mutex::new(None),
            selftest_out: selftest_out.clone(),
        })
        .setup(move |app| {
            let state = app.state::<AppState>();
            let resources = app.path().resource_dir()?;
            match spawn_core(&resources) {
                Ok(core) => {
                    *state.core_ready_ms.lock().unwrap() = Some(launched.elapsed().as_millis());
                    *state.core.lock().unwrap() = Some(core);
                }
                Err(error) => *state.core_error.lock().unwrap() = Some(error),
            }
            if let Some(path) = selftest_out.clone() {
                let handle = app.handle().clone();
                std::thread::spawn(move || {
                    std::thread::sleep(SELFTEST_TIMEOUT);
                    let _ = std::fs::write(
                        &path,
                        br#"{"via_webview": false, "error": "page never reported"}"#,
                    );
                    handle.exit(1);
                });
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![ping_core, report_ui])
        .build(tauri::generate_context!())
        .expect("failed to build the Tauri application");

    app.run(|handle, event| {
        if let RunEvent::Exit = event {
            let state = handle.state::<AppState>();
            let core = state.core.lock().unwrap().take();
            if let Some(core) = core {
                let how = core.shutdown();
                eprintln!("core {how}");
            }
        }
    });
}
