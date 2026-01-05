import os
import tempfile
import pytest
from src.storage import Storage

def test_create_and_list_task():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "t.db")
        s = Storage(db)

        tid = s.create_task("Primeira", "desc", priority="media")
        tasks = s.list_tasks()

        assert len(tasks) == 1
        assert tasks[0]["id"] == tid
        assert tasks[0]["title"] == "Primeira"

def test_update_task():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "t.db")
        s = Storage(db)

        tid = s.create_task("A", None)
        s.update_task(tid, title="B", status="done")
        tasks = s.list_tasks()
        assert tasks[0]["title"] == "B"
        assert tasks[0]["status"] == "done"

def test_delete_task():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "t.db")
        s = Storage(db)

        tid = s.create_task("A", None)
        s.delete_task(tid)
        assert s.list_tasks() == []

def test_scope_change_critical_requires_deadline():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "t.db")
        s = Storage(db)

        with pytest.raises(ValueError):
            s.create_task("Urgente", "x", priority="critica", deadline=None)

        tid = s.create_task("Urgente", "x", priority="critica", deadline="2026-01-31")
        assert tid > 0
