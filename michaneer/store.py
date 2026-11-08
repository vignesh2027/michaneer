"""Local log of bucket tests, so a household can see a measured change.

Stored in SQLite on the user's own machine. Only the readings and a short
label are kept, never a name, phone number or address.
"""

from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from .model import Readings, evaluate

DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "michaneer.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    label TEXT NOT NULL,
    readings TEXT NOT NULL,
    recovery REAL NOT NULL,
    annual_reject_l REAL NOT NULL
)
"""


@dataclass(frozen=True)
class Entry:
    id: int
    created_at: str
    label: str
    readings: Readings
    recovery: float
    annual_reject_l: float


def db_path() -> Path:
    return Path(os.environ.get("MICHANEER_DB", DEFAULT_DB))


def _connect() -> sqlite3.Connection:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    return conn


def add(readings: Readings, label: str) -> int:
    result = evaluate(readings)
    label = " ".join(label.split())[:60] or "Bucket test"
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO tests (created_at, label, readings, recovery, annual_reject_l) VALUES (?, ?, ?, ?, ?)",
            (
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                label,
                json.dumps(asdict(readings)),
                result.recovery,
                result.annual_reject_l,
            ),
        )
        return int(cur.lastrowid)


def all_entries() -> list[Entry]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, created_at, label, readings, recovery, annual_reject_l FROM tests ORDER BY id"
        ).fetchall()
    return [
        Entry(row[0], row[1], row[2], Readings(**json.loads(row[3])), row[4], row[5])
        for row in rows
    ]


def delete(entry_id: int) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM tests WHERE id = ?", (entry_id,))


def clear() -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM tests")


class MemoryLog:
    """Log for the hosted demo: kept in server memory per browser, never on disk.

    Each browser gets a random id in a cookie. Entries vanish when the demo
    container restarts or scales to zero, and old browsers are dropped first.
    """

    MAX_BROWSERS = 500
    MAX_ENTRIES = 20

    def __init__(self) -> None:
        self._logs: dict[str, list[Entry]] = {}
        self._next_id = 1

    def add(self, owner: str, readings: Readings, label: str) -> int:
        result = evaluate(readings)
        label = " ".join(label.split())[:60] or "Bucket test"
        log = self._logs.pop(owner, [])
        self._logs[owner] = log  # most recently used last
        while len(self._logs) > self.MAX_BROWSERS:
            self._logs.pop(next(iter(self._logs)))
        entry = Entry(self._next_id, datetime.now(timezone.utc).isoformat(timespec="seconds"), label,
                      readings, result.recovery, result.annual_reject_l)
        self._next_id += 1
        log.append(entry)
        del log[:-self.MAX_ENTRIES]
        return entry.id

    def all_entries(self, owner: str | None) -> list[Entry]:
        return list(self._logs.get(owner or "", []))

    def delete(self, owner: str | None, entry_id: int) -> None:
        log = self._logs.get(owner or "")
        if log is not None:
            log[:] = [e for e in log if e.id != entry_id]
