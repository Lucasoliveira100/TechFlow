import sqlite3
from typing import Optional, List, Dict, Any

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  priority TEXT NOT NULL DEFAULT 'media',
  status TEXT NOT NULL DEFAULT 'to_do',
  assignee TEXT,
  deadline TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

class Storage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._conn() as con:
            con.execute(DB_SCHEMA)

    def create_task(self, title: str, description: str | None, priority: str = "media",
                    status: str = "to_do", assignee: str | None = None, deadline: str | None = None) -> int:
        self._validate_priority_deadline(priority, deadline)
        with self._conn() as con:
            cur = con.execute(
                "INSERT INTO tasks(title, description, priority, status, assignee, deadline) VALUES(?,?,?,?,?,?)",
                (title, description, priority, status, assignee, deadline),
            )
            return int(cur.lastrowid)

    def list_tasks(self) -> List[Dict[str, Any]]:
        with self._conn() as con:
            con.row_factory = sqlite3.Row
            rows = con.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
            return [dict(r) for r in rows]

    def update_task(self, task_id: int, **fields) -> None:
        allowed = {"title", "description", "priority", "status", "assignee", "deadline"}
        set_parts = []
        values = []

        if "priority" in fields or "deadline" in fields:
            self._validate_priority_deadline(fields.get("priority"), fields.get("deadline"))

        for k, v in fields.items():
            if k in allowed:
                set_parts.append(f"{k}=?")
                values.append(v)

        if not set_parts:
            return

        values.append(task_id)
        with self._conn() as con:
            con.execute(f"UPDATE tasks SET {', '.join(set_parts)} WHERE id=?", values)

    def delete_task(self, task_id: int) -> None:
        with self._conn() as con:
            con.execute("DELETE FROM tasks WHERE id=?", (task_id,))

    def _validate_priority_deadline(self, priority: Optional[str], deadline: Optional[str]) -> None:
        # Mudança de escopo: se prioridade for "critica", deadline é obrigatório
        if priority is not None and priority.lower() == "critica" and not deadline:
            raise ValueError("Tarefas com prioridade 'critica' precisam de deadline (YYYY-MM-DD).")
