import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from gateway.config import Platform, PlatformConfig
from gateway.platforms.telegram import TelegramAdapter
from gateway import task_panel


def _source():
    return SimpleNamespace(
        platform=Platform.TELEGRAM,
        chat_id="-1003772186616",
        thread_id="92",
        message_id="123",
        user_id="u1",
        user_name="Mikhail",
    )


def test_create_list_update_close_lifecycle(tmp_path):
    db = tmp_path / "tasks.db"

    created = task_panel.create_task(
        "Сделать MVP TODO",
        source=_source(),
        reply_to_message_id="99",
        reply_to_text="исходный контекст",
        db_path=db,
    )

    assert created["status"] == "Триаж"
    assert created["priority"] == "P1"
    assert created["context"] == "исходный контекст"
    assert created["next_step"]

    active = task_panel.list_tasks(db_path=db)
    assert [task["id"] for task in active] == [created["id"]]

    started = task_panel.apply_callback("start", created["id"], actor="Bud", db_path=db)
    assert "Статус: В работе" in started.text

    closed = task_panel.handle_command(
        "done",
        "",
        source=_source(),
        reply_to_message_id="99",
        db_path=db,
    )
    assert closed.task_id == created["id"]
    assert "Статус: Закрыто" in closed.text
    assert task_panel.list_tasks(db_path=db) == []


def test_buttons_match_mvp_labels_and_callback_shape():
    rows = task_panel.button_rows("tsk_1")
    labels = [label for row in rows for label, _ in row]
    assert labels == [
        "▶️ В работу",
        "✅ Закрыть",
        "⛔ Блокер",
        "⏰ Пересмотр",
        "🔥 Приоритет",
        "👤 Назначить",
        "🧵 Контекст",
        "📝 История",
    ]
    assert task_panel.parse_callback_data("tp:block:tsk_1") == ("block", "tsk_1")


def test_command_create_from_reply_and_stale_digest(tmp_path):
    db = tmp_path / "tasks.db"
    response = task_panel.handle_command(
        "task",
        "",
        source=_source(),
        reply_to_message_id="77",
        reply_to_text="reply text becomes task title",
        db_path=db,
    )
    assert response.show_keyboard is True
    assert response.task_id
    assert "reply text becomes task title" in response.text

    task_panel.update_task(
        response.task_id,
        review_at="2000-01-01T00:00:00+03:00",
        actor="test",
        db_path=db,
    )
    stale = task_panel.handle_command("stale", "", source=_source(), db_path=db)
    assert "Stale/watchdog" in stale.text
    assert response.task_id in stale.text


def test_context_and_history_rendering(tmp_path):
    db = tmp_path / "tasks.db"
    task = task_panel.create_task(
        "Проверить контекст",
        source=_source(),
        reply_to_text="важный контекст",
        db_path=db,
    )

    context = task_panel.apply_callback("context", task["id"], actor="Bud", db_path=db)
    history = task_panel.apply_callback("history", task["id"], actor="Bud", db_path=db)

    assert "важный контекст" in context.text
    assert "created" in history.text


def test_source_and_panel_message_ids_support_reply_done(tmp_path):
    db = tmp_path / "tasks.db"
    created = task_panel.handle_command(
        "task",
        "task from command",
        source=_source(),
        source_message_id="500",
        db_path=db,
    )
    task_panel.update_task(created.task_id, panel_message_id="600", db_path=db)

    by_source = task_panel.handle_command("done", "", reply_to_message_id="500", source=_source(), db_path=db)
    assert by_source.task_id == created.task_id
    assert "Статус: Закрыто" in by_source.text

    created_again = task_panel.handle_command(
        "task",
        "second task",
        source=_source(),
        source_message_id="501",
        db_path=db,
    )
    task_panel.update_task(created_again.task_id, panel_message_id="601", db_path=db)
    by_panel = task_panel.handle_command("done", "", reply_to_message_id="601", source=_source(), db_path=db)
    assert by_panel.task_id == created_again.task_id
    assert "Статус: Закрыто" in by_panel.text


def test_callback_scope_must_match_source_chat_and_thread(tmp_path):
    db = tmp_path / "tasks.db"
    task = task_panel.create_task("Scoped", source=_source(), db_path=db)

    assert task_panel.task_matches_scope(task, chat_id="-1003772186616", thread_id="92") is True
    assert task_panel.task_matches_scope(task, chat_id="-1003772186616", thread_id="1346") is False
    assert task_panel.task_matches_scope(task, chat_id="-1001", thread_id="92") is False


def test_telegram_callback_handler_updates_task_and_edits_message(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENTIC_STACK_TASKS_DB", str(tmp_path / "tasks.db"))
    task = task_panel.create_task("Проверить callback", source=_source())

    adapter = object.__new__(TelegramAdapter)
    adapter.platform = Platform.TELEGRAM
    adapter.config = PlatformConfig(enabled=True, token="***", extra={})
    adapter._message_handler = None

    query = MagicMock()
    query.data = f"tp:start:{task['id']}"
    query.message.chat_id = -1003772186616
    query.message.message_thread_id = 92
    query.message.chat.type = "supergroup"
    query.from_user.id = 123
    query.from_user.username = "Bud"
    query.from_user.full_name = "Bud Askins"
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()

    update = MagicMock()
    update.callback_query = query

    asyncio.run(adapter._handle_callback_query(update, MagicMock()))

    assert task_panel.get_task(task["id"])["status"] == "В работе"
    query.answer.assert_awaited_once_with(text="Готово")
    call_args = query.edit_message_text.call_args
    assert call_args is not None
    edit_kwargs = call_args.kwargs
    assert "Статус: В работе" in edit_kwargs["text"]
    assert edit_kwargs["reply_markup"] is not None
