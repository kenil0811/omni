// EXP-PACKAGE: prove WebView -> Rust host -> bundled Python works end to end.
const { invoke } = window.__TAURI__.core;
const status = document.getElementById("status");
const detail = document.getElementById("detail");

async function run() {
  let result;
  try {
    result = await invoke("ping_core");
    status.textContent = `Platform service running: Python ${result.python}`;
    status.className = "ok";
  } catch (error) {
    result = { error: String(error) };
    status.textContent = `Platform service failed: ${error}`;
    status.className = "bad";
  }
  detail.textContent = JSON.stringify(result, null, 2);
  // Only acted on in --selftest mode; ignored otherwise.
  await invoke("report_ui", { result, rendered: status.textContent });
}

run();
