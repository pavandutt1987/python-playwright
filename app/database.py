import sqlite3
import os
import tempfile
from contextlib import closing, contextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

APP_DB_FILE = os.path.join(os.path.dirname(__file__), "history.db")


def _user_db_file() -> str:
    """Return a persistent, user-writable location for application data."""
    data_dir = os.environ.get("LOCALAPPDATA")
    if not data_dir:
        data_dir = os.path.join(os.path.expanduser("~"), ".local", "share")
    return os.path.join(data_dir, "PlaywrightPracticeStudio", "history.db")


def _can_write_path(path: str) -> bool:
    """SQLite needs write access to both its file and journal directory."""
    parent = os.path.dirname(os.path.abspath(path))
    try:
        os.makedirs(parent, exist_ok=True)
        if os.path.exists(path):
            # Opening in append mode detects Windows' ReadOnly attribute.
            with open(path, "ab"):
                pass
        with tempfile.TemporaryFile(dir=parent):
            pass
        return True
    except OSError:
        return False


def _select_db_file() -> str:
    configured_path = os.environ.get("PLAYWRIGHT_STUDIO_DB")
    if configured_path:
        configured_path = os.path.abspath(os.path.expanduser(os.path.expandvars(configured_path)))
        os.makedirs(os.path.dirname(configured_path), exist_ok=True)
        return configured_path

    if _can_write_path(APP_DB_FILE):
        return APP_DB_FILE

    fallback_path = _user_db_file()
    fallback_parent = os.path.dirname(fallback_path)
    os.makedirs(fallback_parent, exist_ok=True)

    # SQLite backup preserves committed data (including WAL contents), without
    # copying ReadOnly attributes. Publish only a complete backup.
    if not os.path.exists(fallback_path) and os.path.exists(APP_DB_FILE):
        fd, backup_path = tempfile.mkstemp(suffix=".db", dir=fallback_parent)
        os.close(fd)
        try:
            source_uri = Path(APP_DB_FILE).resolve().as_uri() + "?mode=ro"
            with closing(sqlite3.connect(source_uri, uri=True)) as source:
                with closing(sqlite3.connect(backup_path)) as destination:
                    source.backup(destination)
            os.replace(backup_path, fallback_path)
        finally:
            if os.path.exists(backup_path):
                os.remove(backup_path)

    return fallback_path


DB_FILE = _select_db_file()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        # Runs history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT NOT NULL,
                code TEXT NOT NULL,
                headed INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL,
                output TEXT,
                duration_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Snippets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                tags TEXT,
                language TEXT NOT NULL,
                code TEXT NOT NULL,
                is_favorite INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# --- Run History operations ---

def record_run(language: str, code: str, headed: bool, status: str, output: str, duration_ms: int) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO runs (language, code, headed, status, output, duration_ms, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (language, code, 1 if headed else 0, status, output, duration_ms, datetime.utcnow().isoformat())
        )
        conn.commit()
        return cursor.lastrowid

def get_recent_runs(language: Optional[str] = None, search: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT id, language, code, headed, status, output, duration_ms, created_at FROM runs WHERE 1=1"
        params = []

        if language and language.lower() != "all":
            query += " AND lower(language) = ?"
            params.append(language.lower())

        if search:
            query += " AND (code LIKE ? OR output LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])

        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def clear_run_history():
    with get_db() as conn:
        conn.cursor().execute("DELETE FROM runs")
        conn.commit()

# --- Snippets operations ---

def create_snippet(title: str, tags: str, language: str, code: str) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.utcnow().isoformat()
        cursor.execute(
            """
            INSERT INTO snippets (title, tags, language, code, is_favorite, created_at, updated_at)
            VALUES (?, ?, ?, ?, 0, ?, ?)
            """,
            (title, tags, language, code, now, now)
        )
        conn.commit()
        snippet_id = cursor.lastrowid
        return get_snippet_by_id(snippet_id)

def get_snippet_by_id(snippet_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM snippets WHERE id = ?", (snippet_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_snippets(language: Optional[str] = None, search: Optional[str] = None, favorites_only: bool = False) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM snippets WHERE 1=1"
        params = []

        if language and language.lower() != "all":
            query += " AND lower(language) = ?"
            params.append(language.lower())

        if favorites_only:
            query += " AND is_favorite = 1"

        if search:
            query += " AND (title LIKE ? OR tags LIKE ? OR code LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

        query += " ORDER BY is_favorite DESC, updated_at DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def update_snippet(snippet_id: int, title: str, tags: str, language: str, code: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.utcnow().isoformat()
        cursor.execute(
            """
            UPDATE snippets
            SET title = ?, tags = ?, language = ?, code = ?, updated_at = ?
            WHERE id = ?
            """,
            (title, tags, language, code, now, snippet_id)
        )
        conn.commit()
        return get_snippet_by_id(snippet_id)

def toggle_favorite_snippet(snippet_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE snippets SET is_favorite = (1 - is_favorite) WHERE id = ?", (snippet_id,))
        conn.commit()
        return get_snippet_by_id(snippet_id)

def delete_snippet(snippet_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
        conn.commit()
        return cursor.rowcount > 0

# Initialize on module import
init_db()
