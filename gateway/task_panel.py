"""Telegram-native Agentic Stack task panel.

This module is intentionally small and independent from the Kanban worker
board. It stores a durable index/control-panel view for Telegram tasks while
execution stays in the source topic.
"""
from __future__ import annotations

import html
import os
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo


MSK = ZoneInfo("Europe/Moscow")
DEFAULT_DB_PATH = Path("/Users/xbr/.agentic-stack/tasks.db")

STATUSES = (
    "Триаж",
    "Очередь",
    "В работе",
    "Блокер",
    "На проверке",
    "Закрыто",
    "Отменено",
)
OPEN_STATUSES = STATUSES[:-2]
PRIORITIES = ("P0", "P1", "P2", "P3")


@dataclass(frozen=True)
class TaskPanelResponse:
    text: str
    task_id: str | None = None
    show_keyboard: bool = False


def _db_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return Path(os.getenv("AGENTIC_STACK_TASKS_DB", str(DEFAULT_DB_PATH)))


def _now_msk() -> datetime:
    return datetime.now(MSK)


def _iso(dt: datetime | None = None) -> str:
    return (dt or _now_msk()).isoformat(timespec="seconds")


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    db_path = _db_path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    init_db(conn)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'P1',
            status TEXT NOT NULL DEFAULT 'Триаж',
            stage TEXT NOT NULL DEFAULT 'Сформулировать',
            responsible TEXT NOT NULL DEFAULT '',
            context TEXT NOT NULL DEFAULT '',
            review_at TEXT NOT NULL DEFAULT '',
            time_limit TEXT NOT NULL DEFAULT '',
            result TEXT NOT NULL DEFAULT '',
            next_step TEXT NOT NULL DEFAULT '',
            source_platform TEXT NOT NULL DEFAULT '',
            source_chat_id TEXT NOT NULL DEFAULT '',
            source_thread_id TEXT NOT NULL DEFAULT '',
            source_message_id TEXT NOT NULL DEFAULT '',
            panel_message_id TEXT NOT NULL DEFAULT '',
            reply_to_message_id TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            closed_at TEXT NOT NULL DEFAULT ''
        )
        """
    )
    _ensure_column(conn, "tasks", "panel_message_id", "TEXT NOT NULL DEFAULT ''")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS task_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            ts TEXT NOT NULL,
            actor TEXT NOT NULL,
            action TEXT NOT NULL,
            detail TEXT NOT NULL DEFAULT '',
            FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
    existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in existing:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def _task_id() -> str:
    return f"tsk_{_now_msk().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(3)}"


def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def _actor(source: Any = None, fallback: str = "") -> str:
    if source is None:
        return fallback or "unknown"
    return (
        str(getattr(source, "user_name", "") or "")
        or str(getattr(source, "user_id", "") or "")
        or fallback
        or "unknown"
    )


def _source_value(source: Any, name: str) -> str:
    value = getattr(source, name, "") if source is not None else ""
    platform = getattr(value, "value", None)
    return str(platform if platform is not None else value or "")


def _insert_event(
    conn: sqlite3.Connection,
    task_id: str,
    action: str,
    *,
    actor: str = "",
    detail: str = "",
) -> None:
    conn.execute(
        "INSERT INTO task_events(task_id, ts, actor, action, detail) VALUES (?, ?, ?, ?, ?)",
        (task_id, _iso(), actor or "unknown", action, detail or ""),
    )


def create_task(
    title: str,
    *,
    source: Any = None,
    reply_to_message_id: str = "",
    reply_to_text: str = "",
    source_message_id: str = "",
    actor: str = "",
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    title = " ".join((title or "").split()).strip()
    if not title:
        raise ValueError("task title is required")
    context = (reply_to_text or "").strip()
    next_step = "Определить владельца и первый конкретный шаг"
    now = _iso()
    task_id = _task_id()
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO tasks(
                id, title, priority, status, stage, responsible, context,
                review_at, time_limit, result, next_step, source_platform,
                source_chat_id, source_thread_id, source_message_id,
                panel_message_id, reply_to_message_id, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                title,
                "P1",
                "Триаж",
                "Сформулировать",
                "",
                context,
                "",
                "",
                "",
                next_step,
                _source_value(source, "platform"),
                _source_value(source, "chat_id"),
                _source_value(source, "thread_id"),
                str(source_message_id or _source_value(source, "message_id")),
                "",
                str(reply_to_message_id or ""),
                now,
                now,
            ),
        )
        _insert_event(conn, task_id, "created", actor=actor or _actor(source), detail=title)
        conn.commit()
        return get_task(task_id, db_path=db_path) or {}


def get_task(task_id: str, *, db_path: str | Path | None = None) -> dict[str, Any] | None:
    with connect(db_path) as conn:
        return _row_to_dict(conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone())


def list_tasks(
    *,
    statuses: Iterable[str] | None = None,
    responsible: str | None = None,
    stale_only: bool = False,
    limit: int = 20,
    db_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    if statuses is None:
        statuses = OPEN_STATUSES
    statuses = tuple(statuses)
    if statuses:
        clauses.append("status IN (%s)" % ",".join("?" for _ in statuses))
        params.extend(statuses)
    if responsible:
        clauses.append("LOWER(responsible) = LOWER(?)")
        params.append(responsible)
    if stale_only:
        clauses.append("review_at != '' AND review_at <= ?")
        params.append(_iso())
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    params.append(max(1, min(int(limit), 50)))
    with connect(db_path) as conn:
        rows = conn.execute(
            f"""
            SELECT * FROM tasks
            {where}
            ORDER BY
                CASE priority WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 WHEN 'P2' THEN 2 ELSE 3 END,
                updated_at DESC
            LIMIT ?
            """,
            params,
        ).fetchall()
        return [dict(row) for row in rows]


def list_events(task_id: str, *, db_path: str | Path | None = None) -> list[dict[str, Any]]:
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM task_events WHERE task_id = ? ORDER BY id DESC LIMIT 12",
            (task_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def update_task(
    task_id: str,
    *,
    actor: str = "",
    db_path: str | Path | None = None,
    event_action: str = "updated",
    event_detail: str = "",
    **fields: Any,
) -> dict[str, Any]:
    allowed = {
        "priority",
        "status",
        "stage",
        "responsible",
        "context",
        "review_at",
        "time_limit",
        "result",
        "next_step",
        "panel_message_id",
        "closed_at",
    }
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        task = get_task(task_id, db_path=db_path)
        if task is None:
            raise KeyError(task_id)
        return task
    if "status" in updates and updates["status"] not in STATUSES:
        raise ValueError(f"invalid task status: {updates['status']}")
    if "priority" in updates and updates["priority"] not in PRIORITIES:
        raise ValueError(f"invalid task priority: {updates['priority']}")
    if updates.get("status") in {"Закрыто", "Отменено"} and not updates.get("closed_at"):
        updates["closed_at"] = _iso()
    updates["updated_at"] = _iso()
    assignments = ", ".join(f"{field} = ?" for field in updates)
    params = list(updates.values()) + [task_id]
    with connect(db_path) as conn:
        cursor = conn.execute(f"UPDATE tasks SET {assignments} WHERE id = ?", params)
        if cursor.rowcount == 0:
            raise KeyError(task_id)
        _insert_event(conn, task_id, event_action, actor=actor, detail=event_detail)
        conn.commit()
    task = get_task(task_id, db_path=db_path)
    if task is None:
        raise KeyError(task_id)
    return task


def find_task_for_reply(
    reply_to_message_id: str,
    *,
    db_path: str | Path | None = None,
) -> dict[str, Any] | None:
    if not reply_to_message_id:
        return None
    with connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT * FROM tasks
            WHERE status NOT IN ('Закрыто', 'Отменено')
              AND (source_message_id = ? OR panel_message_id = ? OR reply_to_message_id = ?)
            ORDER BY updated_at DESC
            LIMIT 1
            """,
            (str(reply_to_message_id), str(reply_to_message_id), str(reply_to_message_id)),
        ).fetchone()
        return _row_to_dict(row)


def task_matches_scope(
    task: dict[str, Any] | None,
    *,
    chat_id: str | None = None,
    thread_id: str | None = None,
) -> bool:
    """Return whether a Telegram callback belongs to the task's source scope."""
    if not task:
        return False
    task_chat = str(task.get("source_chat_id") or "")
    task_thread = str(task.get("source_thread_id") or "")
    if task_chat and chat_id is not None and task_chat != str(chat_id):
        return False
    if task_thread and thread_id is not None and task_thread != str(thread_id):
        return False
    return True


def next_priority(priority: str) -> str:
    order = ("P2", "P1", "P0")
    try:
        return order[(order.index(priority) + 1) % len(order)]
    except ValueError:
        return "P1"


def apply_callback(
    action: str,
    task_id: str,
    *,
    actor: str = "",
    db_path: str | Path | None = None,
) -> TaskPanelResponse:
    task = get_task(task_id, db_path=db_path)
    if task is None:
        return TaskPanelResponse("Задача не найдена или уже удалена.")
    if action == "start":
        task = update_task(
            task_id,
            status="В работе",
            stage="Исполнение",
            actor=actor,
            event_action="started",
            event_detail="inline button",
            db_path=db_path,
        )
    elif action == "close":
        task = update_task(
            task_id,
            status="Закрыто",
            stage="Готово",
            result=task.get("result") or "Закрыто через Telegram",
            actor=actor,
            event_action="closed",
            event_detail="inline button",
            db_path=db_path,
        )
    elif action == "block":
        task = update_task(
            task_id,
            status="Блокер",
            stage="Нужен unblock",
            actor=actor,
            event_action="blocked",
            event_detail="inline button",
            db_path=db_path,
        )
    elif action == "review":
        review_at = _iso(_now_msk() + timedelta(hours=2))
        task = update_task(
            task_id,
            review_at=review_at,
            actor=actor,
            event_action="review_scheduled",
            event_detail=review_at,
            db_path=db_path,
        )
    elif action == "prio":
        new_priority = next_priority(task.get("priority", "P1"))
        task = update_task(
            task_id,
            priority=new_priority,
            actor=actor,
            event_action="priority_changed",
            event_detail=new_priority,
            db_path=db_path,
        )
    elif action == "assign":
        task = update_task(
            task_id,
            responsible=actor or "unknown",
            actor=actor,
            event_action="assigned",
            event_detail=actor or "unknown",
            db_path=db_path,
        )
    elif action == "context":
        return TaskPanelResponse(render_context(task), task_id=task_id, show_keyboard=True)
    elif action == "history":
        return TaskPanelResponse(render_history(task_id, db_path=db_path), task_id=task_id, show_keyboard=True)
    else:
        return TaskPanelResponse("Неизвестное действие.")
    return TaskPanelResponse(render_card(task), task_id=task_id, show_keyboard=True)


def handle_command(
    command: str,
    args: str,
    *,
    source: Any = None,
    reply_to_message_id: str = "",
    reply_to_text: str = "",
    source_message_id: str = "",
    db_path: str | Path | None = None,
) -> TaskPanelResponse:
    command = command.strip().lower()
    args = (args or "").strip()
    actor = _actor(source)
    if command == "task":
        title = args or (reply_to_text or "").strip()
        if not title:
            return TaskPanelResponse("Формат: /task <текст> или reply + /task")
        task = create_task(
            title,
            source=source,
            reply_to_message_id=reply_to_message_id,
            reply_to_text=reply_to_text if args else "",
            source_message_id=source_message_id,
            actor=actor,
            db_path=db_path,
        )
        return TaskPanelResponse(render_card(task), task_id=task["id"], show_keyboard=True)
    if command == "tasks":
        return TaskPanelResponse(render_list(list_tasks(db_path=db_path), title="Задачи"))
    if command == "mine":
        return TaskPanelResponse(
            render_list(list_tasks(responsible=actor, db_path=db_path), title="Мои задачи")
        )
    if command == "stale":
        return TaskPanelResponse(
            render_digest(list_tasks(stale_only=True, db_path=db_path))
        )
    if command == "done":
        task_id = args.split()[0] if args else ""
        task = get_task(task_id, db_path=db_path) if task_id else None
        if task is None and reply_to_message_id:
            task = find_task_for_reply(reply_to_message_id, db_path=db_path)
        if task is None:
            return TaskPanelResponse("Не нашёл задачу. Используй reply + /done или /done <id>.")
        closed = update_task(
            task["id"],
            status="Закрыто",
            stage="Готово",
            result="Закрыто через /done",
            actor=actor,
            event_action="closed",
            event_detail="/done",
            db_path=db_path,
        )
        return TaskPanelResponse(render_card(closed), task_id=closed["id"], show_keyboard=True)
    return TaskPanelResponse("Неизвестная TODO-команда.")


def button_rows(task_id: str) -> list[list[tuple[str, str]]]:
    return [
        [("▶️ В работу", f"tp:start:{task_id}"), ("✅ Закрыть", f"tp:close:{task_id}")],
        [("⛔ Блокер", f"tp:block:{task_id}"), ("⏰ Пересмотр", f"tp:review:{task_id}")],
        [("🔥 Приоритет", f"tp:prio:{task_id}"), ("👤 Назначить", f"tp:assign:{task_id}")],
        [("🧵 Контекст", f"tp:context:{task_id}"), ("📝 История", f"tp:history:{task_id}")],
    ]


def parse_callback_data(data: str) -> tuple[str, str] | None:
    parts = (data or "").split(":", 2)
    if len(parts) != 3 or parts[0] != "tp":
        return None
    return parts[1], parts[2]


def _field(value: Any, default: str = "—") -> str:
    text = str(value or "").strip()
    return text or default


def render_card(task: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"Задача {task['id']}: {_field(task.get('title'))}",
            f"Приоритет: {_field(task.get('priority'))}",
            f"Статус: {_field(task.get('status'))}",
            f"Этап: {_field(task.get('stage'))}",
            f"Ответственный: {_field(task.get('responsible'))}",
            f"Контекст: {_short(_field(task.get('context')), 220)}",
            f"Пересмотр: {_field(task.get('review_at'))}",
            f"Лимит времени: {_field(task.get('time_limit'))}",
            f"Результат: {_field(task.get('result'))}",
            f"Следующий шаг: {_field(task.get('next_step'))}",
        ]
    )


def render_card_html(task: dict[str, Any]) -> str:
    lines = render_card(task).splitlines()
    if not lines:
        return ""
    first = f"<b>{html.escape(lines[0])}</b>"
    return "\n".join([first, *(html.escape(line) for line in lines[1:])])


def render_context(task: dict[str, Any]) -> str:
    context = _field(task.get("context"), "Контекст не сохранён")
    source = " / ".join(
        part
        for part in [
            _field(task.get("source_platform"), ""),
            _field(task.get("source_chat_id"), ""),
            _field(task.get("source_thread_id"), ""),
            _field(task.get("source_message_id"), ""),
        ]
        if part
    )
    return f"Контекст {task['id']}\n{context}\n\nИсточник: {source or '—'}"


def render_history(task_id: str, *, db_path: str | Path | None = None) -> str:
    events = list_events(task_id, db_path=db_path)
    if not events:
        return f"История {task_id}: пусто"
    lines = [f"История {task_id}"]
    for event in events:
        detail = f" — {event['detail']}" if event.get("detail") else ""
        lines.append(f"{event['ts']} · {event['actor']} · {event['action']}{detail}")
    return "\n".join(lines)


def render_list(tasks: list[dict[str, Any]], *, title: str = "Задачи") -> str:
    if not tasks:
        return f"{title}: пусто"
    lines = [title]
    for task in tasks[:12]:
        owner = _field(task.get("responsible"))
        lines.append(
            f"{task['priority']} · {task['status']} · {task['id']} · "
            f"{_short(task['title'], 80)} · {owner}"
        )
    return "\n".join(lines)


def render_digest(tasks: list[dict[str, Any]]) -> str:
    if not tasks:
        return "Stale/watchdog: пусто"
    focus = tasks[:3]
    lines = ["Stale/watchdog"]
    for task in focus:
        lines.append(
            f"{task['priority']} · {task['status']} · {task['id']} · "
            f"{_short(task['title'], 80)}"
        )
    if len(tasks) > 3:
        lines.append(f"Позже: ещё {len(tasks) - 3}")
    return "\n".join(lines)


def _short(text: str, limit: int) -> str:
    text = " ".join(str(text or "").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"
