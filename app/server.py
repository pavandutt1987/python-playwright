import os
import sys
import uuid
import json
import asyncio
import subprocess
import sqlite3
import logging
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import database as db
from . import templates
from . import runner

app = FastAPI(title="Playwright Practice Studio API")

# The UI and desktop are served from the same origin by the cloud proxy.
PUBLIC_ORIGIN = os.environ.get("STUDIO_PUBLIC_ORIGIN", "").rstrip("/")


@app.middleware("http")
async def check_write_origin(request, call_next):
    if PUBLIC_ORIGIN and request.method not in {"GET", "HEAD", "OPTIONS"}:
        if request.headers.get("origin") != PUBLIC_ORIGIN:
            return JSONResponse({"detail": "Origin not allowed"}, status_code=403)
    return await call_next(request)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
PLAYGROUND_DIR = os.path.join(STATIC_DIR, "playground")

# Mount static folders
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/playground", StaticFiles(directory=PLAYGROUND_DIR), name="playground")

# Request Models
class SnippetCreate(BaseModel):
    title: str
    tags: Optional[str] = ""
    language: str
    code: str

class SnippetUpdate(BaseModel):
    title: str
    tags: Optional[str] = ""
    language: str
    code: str

class StopRequest(BaseModel):
    execution_id: str

# --- Page Routes ---

@app.get("/")
async def get_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_file)

# --- Status / Health Check ---

@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/status")
async def get_status():
    # 1. Check Python Playwright
    python_playwright = False
    try:
        import playwright
        python_playwright = True
    except ImportError:
        pass

    # 2. Check Node & TSX
    node_installed = False
    tsx_installed = False
    try:
        node_res = subprocess.run(["node", "--version"], capture_output=True, text=True)
        node_installed = node_res.returncode == 0
    except Exception:
        pass

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tsx_cmd = os.path.join(project_root, "node_modules", "tsx", "dist", "cli.mjs")
    tsx_installed = os.path.exists(tsx_cmd) or shutil_which("tsx")

    # 3. Check Chromium browser
    chromium_installed = False
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as pw:
            chromium_installed = os.path.isfile(pw.chromium.executable_path)
    except Exception:
        pass

    return {
        "python_playwright": python_playwright,
        "node": node_installed,
        "tsx": tsx_installed,
        "chromium": chromium_installed,
        "remote_desktop": os.environ.get("STUDIO_REMOTE_DESKTOP") == "1",
        "desktop_url": "/desktop/vnc.html?autoconnect=true&resize=scale&path=desktop/websockify",
        "max_runs": runner.MAX_RUNS,
        "timeout_seconds": runner.DEFAULT_TIMEOUT,
    }

def shutil_which(cmd: str) -> bool:
    import shutil
    return shutil.which(cmd) is not None

# --- Challenge Templates ---

@app.get("/api/templates")
async def list_templates():
    return templates.get_template_list()

@app.get("/api/templates/{template_id}")
async def get_template(template_id: str, lang: str = "python"):
    code = templates.get_template_code(template_id, lang)
    return {"template_id": template_id, "language": lang, "code": code}

# --- Code Execution WebSocket ---

@app.websocket("/ws/run")
async def websocket_run_code(websocket: WebSocket):
    if PUBLIC_ORIGIN and websocket.headers.get("origin") != PUBLIC_ORIGIN:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    execution_id = uuid.uuid4().hex
    disconnect_task = None
    execution_task = None

    async def watch_disconnect():
        while True:
            message = await websocket.receive()
            if message["type"] == "websocket.disconnect":
                return

    async def stream_execution(language, code, headed):
        result = None
        async for item in runner.execute_code_stream(execution_id, language, code, headed=headed):
            if item.get("type") == "done":
                result = item
            else:
                await websocket.send_json(item)
        return result

    try:
        data = await asyncio.wait_for(websocket.receive_text(), timeout=15)
        payload = json.loads(data)
        if not isinstance(payload, dict):
            raise ValueError("Expected a code execution object")

        language = payload.get("language", "python")
        code = payload.get("code", "")
        headed = payload.get("headed", False)
        if language not in {"python", "javascript", "typescript", "js", "ts"}:
            raise ValueError("Unsupported language")
        if not isinstance(code, str) or not code.strip() or len(code.encode("utf-8")) > 200_000:
            raise ValueError("Code must be nonempty and at most 200 KB")
        if not isinstance(headed, bool):
            raise ValueError("headed must be a boolean")

        await websocket.send_json({"execution_id": execution_id})

        disconnect_task = asyncio.create_task(watch_disconnect())
        execution_task = asyncio.create_task(stream_execution(language, code, headed))
        done, _ = await asyncio.wait(
            {disconnect_task, execution_task}, return_when=asyncio.FIRST_COMPLETED
        )
        if disconnect_task in done:
            return
        final_result = await execution_task
        if final_result is None:
            return

        # Save before notifying the UI to refresh history. A storage failure must
        # not replace the actual test result with a second, failed completion.
        try:
            db.record_run(
                language=language,
                code=code,
                headed=headed,
                status=final_result["status"],
                output=final_result.get("full_output", ""),
                duration_ms=final_result["duration_ms"]
            )
        except sqlite3.Error as e:
            logging.getLogger(__name__).warning("Could not save run history", exc_info=True)
            await websocket.send_json({
                "type": "log",
                "text": f"⚠️ Could not save run history to {db.DB_FILE}: {e}\n"
            })
        if final_result is not None:
            await websocket.send_json(final_result)

    except WebSocketDisconnect:
        await runner.stop_execution(execution_id)
    except Exception as e:
        import traceback
        traceback.print_exc()
        await websocket.send_json({
            "type": "error",
            "text": f"Execution failed with internal server error: {str(e)}"
        })
        await websocket.send_json({
            "type": "done",
            "status": "failed",
            "duration_ms": 0
        })
    finally:
        for task in (execution_task, disconnect_task):
            if task is not None and not task.done():
                task.cancel()
        await asyncio.gather(
            *(task for task in (execution_task, disconnect_task) if task is not None),
            return_exceptions=True,
        )
        await runner.stop_execution(execution_id)
        try:
            await websocket.close()
        except (RuntimeError, WebSocketDisconnect):
            pass

@app.post("/api/stop")
async def stop_code_execution(req: StopRequest):
    stopped = await runner.stop_execution(req.execution_id)
    return {"stopped": stopped}

# --- History Endpoints ---

@app.get("/api/history")
async def get_history(language: Optional[str] = None, search: Optional[str] = None):
    return db.get_recent_runs(language=language, search=search)

@app.delete("/api/history")
async def clear_history():
    db.clear_run_history()
    return {"cleared": True}

# --- Snippet Library Endpoints ---

@app.get("/api/snippets")
async def get_snippets(language: Optional[str] = None, search: Optional[str] = None, favorites_only: bool = False):
    return db.get_all_snippets(language=language, search=search, favorites_only=favorites_only)

@app.post("/api/snippets")
async def create_new_snippet(snippet: SnippetCreate):
    created = db.create_snippet(
        title=snippet.title,
        tags=snippet.tags or "",
        language=snippet.language,
        code=snippet.code
    )
    return created

@app.put("/api/snippets/{snippet_id}")
async def update_existing_snippet(snippet_id: int, snippet: SnippetUpdate):
    updated = db.update_snippet(
        snippet_id=snippet_id,
        title=snippet.title,
        tags=snippet.tags or "",
        language=snippet.language,
        code=snippet.code
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return updated

@app.put("/api/snippets/{snippet_id}/favorite")
async def toggle_favorite(snippet_id: int):
    updated = db.toggle_favorite_snippet(snippet_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return updated

@app.delete("/api/snippets/{snippet_id}")
async def delete_existing_snippet(snippet_id: int):
    deleted = db.delete_snippet(snippet_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return {"deleted": True}

# --- Mock APIs for Playground Targets ---

@app.get("/api/products/more")
async def mock_more_products(id: int = 105):
    # Simulate network latency for AJAX practice
    await asyncio.sleep(1.0)
    return [
        {"id": id, "name": "4K Ultra HD Webcam", "category": "Accessories", "price": "$89.99", "status": "In Stock"},
        {"id": id + 1, "name": "USB-C Dual Display Dock", "category": "Electronics", "price": "$159.00", "status": "In Stock"},
        {"id": id + 2, "name": "Studio Condenser Microphone", "category": "Audio", "price": "$119.50", "status": "In Stock"}
    ]

@app.get("/api/user-profile")
async def mock_user_profile():
    # Default mock user profile (interceptable via Playwright page.route)
    return {
        "name": "Alex Mercer",
        "role": "Principal Automation Engineer",
        "department": "Quality & Platform",
        "status": "Active VIP"
    }
