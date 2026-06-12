"""Codex gpt-5.5 compaction autoraise should not spam gateway chats."""

from __future__ import annotations

from run_agent import AIAgent


def test_codex_gpt55_autoraise_applies_without_gateway_replay() -> None:
    """Keep the 85% threshold auto-tune, but do not replay its info notice.

    The notice is helpful for CLI startup output, but in gateway sessions it was
    delivered as a standalone Telegram/Slack/Discord message on the first turn.
    That path should be reserved for actionable compression warnings.
    """

    callback_events: list[tuple[str, str]] = []
    agent = AIAgent(
        model="gpt-5.5",
        provider="openai-codex",
        base_url="https://chatgpt.com/backend-api/codex",
        api_key="sk-test",
        quiet_mode=True,
        enabled_toolsets=[],
        status_callback=lambda event, message: callback_events.append((event, message)),
        skip_context_files=True,
        skip_memory=True,
    )

    assert getattr(agent, "_compression_threshold_autoraised", None) == {
        "from": 0.50,
        "to": 0.85,
    }
    assert agent.context_compressor.threshold_percent == 0.85
    assert agent._compression_warning is None

    agent._replay_compression_warning()

    assert callback_events == []
