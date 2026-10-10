import asyncio
import os
import sys
import time
import subprocess
import shutil
import tempfile
import json
import re
from typing import Dict, Tuple, AsyncGenerator, Any

# Directory to hold temporary execution files (outside workspace to avoid watcher reloads)
WORKSPACE_DIR = os.path.join(tempfile.gettempdir(), "playwright_practice_studio_runs")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

ACTIVE_PROCESSES: Dict[str, asyncio.subprocess.Process] = {}

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
    timeout_sec: int = 60
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Executes Python, JavaScript, or TypeScript code asynchronously,
    streaming output line-by-line and handling process termination cleanly.
    """
    lang = language.lower()
    start_time = time.time()
    project_root = get_project_root()

    uses_test_runner = lang in ["typescript", "ts", "javascript", "js"] and is_playwright_test(code)
    if lang == "python":
        ext = ".py"
    elif uses_test_runner:
        ext = ".spec.ts" if lang in ["typescript", "ts"] else ".spec.js"
    else:
        ext = ".ts" if lang in ["typescript", "ts"] else ".js"
    file_name = f"run_{execution_id}{ext}"
    run_dir = None

    try:
        # Isolate discovery and artifacts so simultaneous runs cannot interfere.
        run_dir = tempfile.mkdtemp(prefix=f"run_{execution_id}_", dir=WORKSPACE_DIR)
        file_path = os.path.join(run_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

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
            cwd=project_root
        )

        ACTIVE_PROCESSES[execution_id] = process
        accumulated_output = []
        output_queue = asyncio.Queue()

        async def pump(stream, is_stderr: bool):
            try:
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    decoded = line.decode("utf-8", errors="replace")
                    await output_queue.put({
                        "type": "error" if is_stderr else "log",
                        "text": decoded,
                        "time": round((time.time() - start_time) * 1000)
                    })
            except Exception:
                pass
            finally:
                await output_queue.put(None)

        task_out = asyncio.create_task(pump(process.stdout, False))
        task_err = asyncio.create_task(pump(process.stderr, True))

        streams_finished = 0
        while streams_finished < 2:
            item = await output_queue.get()
            if item is None:
                streams_finished += 1
            else:
                accumulated_output.append(item["text"])
                yield item

        await asyncio.gather(task_out, task_err, return_exceptions=True)
        await asyncio.wait_for(process.wait(), timeout=5.0)

        duration_ms = int((time.time() - start_time) * 1000)
        status = "success" if process.returncode == 0 else "failed"

        yield {
            "type": "done",
            "status": status,
            "exit_code": process.returncode,
            "duration_ms": duration_ms,
            "full_output": "".join(accumulated_output)
        }

    except asyncio.CancelledError:
        await stop_execution(execution_id)
        duration_ms = int((time.time() - start_time) * 1000)
        yield {
            "type": "done",
            "status": "stopped",
            "exit_code": -1,
            "duration_ms": duration_ms,
            "full_output": "\n🛑 Execution manually aborted by user."
        }
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        yield {
            "type": "done",
            "status": "failed",
            "exit_code": 1,
            "duration_ms": duration_ms,
            "full_output": f"\n💥 Execution Error: {str(e)}"
        }
    finally:
        ACTIVE_PROCESSES.pop(execution_id, None)
        if run_dir:
            shutil.rmtree(run_dir, ignore_errors=True)

async def stop_execution(execution_id: str) -> bool:
    """Terminates an active child process."""
    process = ACTIVE_PROCESSES.get(execution_id)
    if not process:
        return False
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)], capture_output=True)
        else:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=2.0)
            except asyncio.TimeoutError:
                process.kill()
        return True
    except Exception:
        return False
