from types import SimpleNamespace

from agent import model_runtime_monitor as monitor
from run_agent import AIAgent


def _cfg(**overrides):
    values = {
        "enabled": True,
        "probe_interval_seconds": 300.0,
        "probe_timeout_seconds": 20.0,
        "notify_cooldown_seconds": 0.0,
        "notify_platform": "telegram",
        "notify_chat_id": "-100",
        "notify_thread_id": "92",
    }
    values.update(overrides)
    return monitor.RuntimeMonitorConfig(**values)


def test_before_llm_call_logs_active_runtime(monkeypatch, caplog):
    monkeypatch.setattr(monitor, "_load_monitor_config", lambda: _cfg())
    agent = SimpleNamespace(
        provider="anthropic",
        model="claude-sonnet-4-5-20250929",
        api_mode="anthropic_messages",
        _fallback_activated=False,
        session_id="s1",
    )

    with caplog.at_level("INFO"):
        monitor.before_llm_call(agent, call_site="unit")

    assert "active runtime before LLM call" in caplog.text
    assert "anthropic/claude-sonnet-4-5-20250929" in caplog.text
    assert "call_site=unit" in caplog.text


def test_on_fallback_activated_records_state_and_notifies(monkeypatch):
    monkeypatch.setattr(monitor, "_load_monitor_config", lambda: _cfg())
    calls = []
    monkeypatch.setattr(monitor, "_notify_once", lambda *args: calls.append(args))
    monkeypatch.setattr(monitor, "_ensure_probe_thread", lambda *args: None)
    agent = SimpleNamespace(
        provider="openai-codex",
        model="gpt-5.5",
        _primary_runtime={"provider": "anthropic", "model": "claude-sonnet"},
        session_id="s1",
    )

    monitor.on_fallback_activated(
        agent,
        reason="rate_limit",
        reason_detail="HTTP 429: Sonnet rate limit exceeded",
        from_provider="anthropic",
        from_model="claude-sonnet",
        to_provider="openai-codex",
        to_model="gpt-5.5",
    )

    assert agent._runtime_monitor_primary_healthy is False
    assert agent._runtime_monitor_last_failure_reason == "rate_limit: HTTP 429: Sonnet rate limit exceeded"
    assert agent._runtime_monitor_next_probe_at > 0
    assert calls
    assert calls[0][2] == "fallback_red"
    assert "anthropic/claude-sonnet → openai-codex/gpt-5.5" in calls[0][3]
    assert "HTTP 429: Sonnet rate limit exceeded" in calls[0][3]


def test_fallback_forwarder_accepts_reason_detail(monkeypatch):
    calls = []

    def fake_try_activate_fallback(agent, reason=None, reason_detail=None):
        calls.append((agent, reason, reason_detail))
        return True

    import agent.chat_completion_helpers as helpers

    monkeypatch.setattr(helpers, "try_activate_fallback", fake_try_activate_fallback)
    dummy = SimpleNamespace()

    assert AIAgent._try_activate_fallback(
        dummy,
        reason="rate_limit",
        reason_detail="HTTP 429: Sonnet rate limit exceeded",
    ) is True
    assert calls == [(dummy, "rate_limit", "HTTP 429: Sonnet rate limit exceeded")]


def test_can_restore_primary_runtime_defers_until_probe_due(monkeypatch):
    monkeypatch.setattr(monitor, "_load_monitor_config", lambda: _cfg())
    monkeypatch.setattr(monitor.time, "monotonic", lambda: 100.0)
    agent = SimpleNamespace(
        _fallback_activated=True,
        _runtime_monitor_primary_healthy=False,
        _runtime_monitor_next_probe_at=200.0,
        provider="openai-codex",
        model="gpt-5.5",
        api_mode="codex_responses",
    )

    assert monitor.can_restore_primary_runtime(agent) is False


def test_can_restore_primary_runtime_allows_after_successful_probe(monkeypatch):
    monkeypatch.setattr(monitor, "_load_monitor_config", lambda: _cfg())
    monkeypatch.setattr(monitor.time, "monotonic", lambda: 500.0)
    monkeypatch.setattr(monitor, "probe_primary", lambda agent, cfg: (True, "ok"))
    notifications = []
    monkeypatch.setattr(monitor, "_notify_once", lambda *args: notifications.append(args))
    agent = SimpleNamespace(
        _fallback_activated=True,
        _runtime_monitor_primary_healthy=False,
        _runtime_monitor_next_probe_at=0.0,
        _primary_runtime={"provider": "anthropic", "model": "claude-sonnet"},
        _rate_limited_until=999.0,
        provider="openai-codex",
        model="gpt-5.5",
        api_mode="codex_responses",
    )

    assert monitor.can_restore_primary_runtime(agent) is True
    assert agent._runtime_monitor_primary_healthy is True
    assert agent._rate_limited_until == 0
    assert notifications[0][2] == "primary_green"
