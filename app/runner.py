import asyncio
import os
import sys
import time
import subprocess
import shutil
import tempfile
import json
import re
import signal
import codecs
from typing import Dict, Tuple, AsyncGenerator, Any

# Directory to hold temporary execution files (outside workspace to avoid watcher reloads)
WORKSPACE_DIR = os.path.join(tempfile.gettempdir(), "playwright_practice_studio_runs")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

ACTIVE_PROCESSES: Dict[str, asyncio.subprocess.Process] = {}
MAX_RUNS = max(1, int(os.environ.get("STUDIO_MAX_RUNS", "1")))
DEFAULT_TIMEOUT = max(1, int(os.environ.get("STUDIO_TIMEOUT_SECONDS", "120")))
MAX_OUTPUT_BYTES = 1_000_000
RESERVED_RUNS = set()
STOPPED_RUNS = set()

def get_project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_node_bin_path() -> Tuple[str, str]:
    """Use Node directly to avoid shell quoting differences on Windows."""
    project_root = get_project_root()
    return "node", os.path.join(project_root, "node_modules", "tsx", "dist", "cli.mjs")


def is_playwright_test(code: str) -> bool:
    """Returns whether the submitted code uses the Playwright Test API."""
    return bool(re.search(
        r"(?:from\s*|require\s*\(\s*)['\"](?:@playwright/test|playwright/test)['\"]",
        code,
    ))

async def execute_code_stream(
    execution_id: str,
    language: str,
    code: str,
    headed: bool = False,
    timeout_sec: int = DEFAULT_TIMEOUT
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Executes Python, JavaScript, or TypeScript code asynchronously,
    streaming output line-by-line and handling process termination cleanly.
    """
    lang = language.lower()
    start_time = time.monotonic()
    project_root = get_project_root()
    if len(RESERVED_RUNS) >= MAX_RUNS:
        yield {"type": "error", "text": "The runner is busy. Wait for the current run to finish.\n"}
        yield {"type": "done", "status": "busy", "duration_ms": 0, "full_output": "Runner busy"}
        return
    RESERVED_RUNS.add(execution_id)

    uses_test_runner = lang in ["typescript", "ts", "javascript", "js"] and is_playwright_test(code)
    if lang == "python":
        ext = ".py"
    elif uses_test_runner:
        ext = ".spec.ts" if lang in ["typescript", "ts"] else ".spec.js"
    else:
        ext = ".ts" if lang in ["typescript", "ts"] else ".js"
    file_name = f"run_{execution_id}{ext}"
    run_dir = None
    tasks = []
    process = None
    accumulated_output = []
    deadline = start_time + timeout_sec

    try:
        # Isolate discovery and artifacts so simultaneous runs cannot interfere.
        run_dir = tempfile.mkdtemp(prefix=f"run_{execution_id}_", dir=WORKSPACE_DIR)
        file_path = os.path.join(run_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        # ESM imports do not use NODE_PATH; expose dependencies beside the script.
        if os.name != "nt":
            os.symlink(os.path.join(project_root, "node_modules"), os.path.join(run_dir, "node_modules"))

        env = os.environ.copy()
        env["HEADED"] = "1" if headed else "0"
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        env["NODE_PATH"] = os.path.join(project_root, "node_modules")

        # Determine command
        if lang == "python":
            python_exe = sys.executable
            cmd = [python_exe, file_path]
        elif uses_test_runner:
            # Playwright Test supplies fixtures and transforms TypeScript itself.
            config_path = os.path.join(run_dir, "playwright.config.cjs")
            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.write("module.exports = " + json.dumps({
                    "testDir": run_dir,
                    "testMatch": file_name,
                    "outputDir": os.path.join(run_dir, "test-results"),
                    "workers": 1,
                    "reporter": "list",
                    "globalTimeout": timeout_sec * 1000,
                }) + ";\n")
            playwright_cli = os.path.join(project_root, "node_modules", "@playwright", "test", "cli.js")
            cmd = ["node", playwright_cli, "test", "--config", config_path]
            if headed:
                cmd.append("--headed")
        elif lang in ["typescript", "ts"]:
            node, tsx_path = get_node_bin_path()
            cmd = [node, tsx_path, file_path]
        else: # javascript
            cmd = ["node", file_path]

        yield {
            "type": "log",
            "text": f"🚀 Starting {language.upper()} Playwright run in {'👁️ HEADED' if headed else '⚡ HEADLESS'} mode...\n",
            "time": 0
        }

        # Spawn child process
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=run_dir,
            start_new_session=os.name != "nt",
        )

        ACTIVE_PROCESSES[execution_id] = process
        output_queue = asyncio.Queue(maxsize=64)

        async def pump(stream, is_stderr: bool):
            decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
            try:
                while True:
                    chunk = await stream.read(4096)
                    decoded = decoder.decode(chunk, final=not chunk)
                    if decoded:
                        await output_queue.put({
                            "type": "error" if is_stderr else "log",
                            "text": decoded,
                            "time": round((time.monotonic() - start_time) * 1000)
                        })
                    if not chunk:
                        break
            except asyncio.CancelledError:
                raise
            else:
                await output_queue.put(None)

        tasks = [asyncio.create_task(pump(process.stdout, False)),
                 asyncio.create_task(pump(process.stderr, True))]

        streams_finished = 0
        output_bytes = 0
        output_limited = False
        while streams_finished < 2:
            item = await asyncio.wait_for(output_queue.get(), timeout=max(0.001, deadline - time.monotonic()))
            if item is None:
                streams_finished += 1
            else:
                output_bytes += len(item["text"].encode("utf-8"))
                if output_bytes > MAX_OUTPUT_BYTES:
                    output_limited = True
                    message = "\nOutput limit exceeded; execution stopped.\n"
                    accumulated_output.append(message)
                    yield {"type": "error", "text": message}
                    await stop_execution(execution_id)
                    break
                accumulated_output.append(item["text"])
                yield item

        if not output_limited:
            await asyncio.wait_for(process.wait(), timeout=max(0.001, deadline - time.monotonic()))

        duration_ms = int((time.monotonic() - start_time) * 1000)
        status = ("output_limit" if output_limited else "stopped" if execution_id in STOPPED_RUNS
                  else "success" if process.returncode == 0 else "failed")

        yield {
            "type": "done",
            "status": status,
            "exit_code": process.returncode,
            "duration_ms": duration_ms,
            "full_output": "".join(accumulated_output)
        }

    except asyncio.TimeoutError:
        await stop_execution(execution_id)
        message = f"\nExecution timed out after {timeout_sec} seconds.\n"
        accumulated_output.append(message)
        yield {"type": "error", "text": message}
        yield {
            "type": "done",
            "status": "timeout",
            "exit_code": -1,
            "duration_ms": int((time.monotonic() - start_time) * 1000),
            "full_output": "".join(accumulated_output)
        }
    except asyncio.CancelledError:
        raise
    except Exception as e:
        duration_ms = int((time.monotonic() - start_time) * 1000)
        message = f"\nExecution error: {e}\n"
        yield {"type": "error", "text": message}
        yield {
            "type": "done",
            "status": "failed",
            "exit_code": 1,
            "duration_ms": duration_ms,
            "full_output": "".join(accumulated_output) + message
        }
    finally:
        await stop_execution(execution_id)
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        if process is not None:
            # Drain closed pipes after a forced stop, including output-limit cases.
            # Windows subprocess transports otherwise outlive their event loop.
            try:
                await asyncio.wait_for(process.communicate(), timeout=5)
            except asyncio.TimeoutError:
                pass
        ACTIVE_PROCESSES.pop(execution_id, None)
        RESERVED_RUNS.discard(execution_id)
        STOPPED_RUNS.discard(execution_id)
        if run_dir:
            shutil.rmtree(run_dir, ignore_errors=True)

async def stop_execution(execution_id: str) -> bool:
    """Terminates an active child process."""
    process = ACTIVE_PROCESSES.get(execution_id)
    if not process:
        return False
    STOPPED_RUNS.add(execution_id)
    try:
        if os.name == "nt":
            if process.returncode is None:
                await asyncio.to_thread(subprocess.run,
                    ["taskkill", "/F", "/T", "/PID", str(process.pid)], capture_output=True)
        else:
            # Each run has a process group, so Chromium descendants are removed too.
            os.killpg(process.pid, signal.SIGKILL)
        await asyncio.wait_for(process.wait(), timeout=5.0)
        return True
    except ProcessLookupError:
        return True
    except Exception:
        return False
