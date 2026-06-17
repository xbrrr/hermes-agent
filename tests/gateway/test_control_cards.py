from gateway.control_cards import (
    format_busy_ack_card,
    format_mm_control_card,
    format_stall_notice_card,
)


def test_control_card_keeps_state_status_next_and_blocker_scannable():
    card = format_mm_control_card(
        state="⏳ Current task running",
        action="queued",
        details=["3 min elapsed", "iteration 2/90", "running: terminal"],
        next_action="I will respond once the current task finishes.",
        blocker="approval needed",
    )

    assert card == (
        "⏳ Current task running — queued\n"
        "Status: 3 min elapsed, iteration 2/90, running: terminal\n"
        "Next: I will respond once the current task finishes.\n"
        "Blocker: approval needed"
    )


def test_busy_ack_card_formats_queue_mode():
    card = format_busy_ack_card(
        mode="queue",
        details=["iteration 4/90", "running: browser"],
    )

    assert card.startswith("⏳ Current task running — queued")
    assert "Status: iteration 4/90, running: browser" in card
    assert "Next: I will respond once the current task finishes." in card


def test_busy_ack_card_formats_subagent_demoted_queue():
    card = format_busy_ack_card(mode="queue", demoted_for_subagents=True)

    assert card.startswith("⏳ Subagent working — queued")
    assert "/stop" in card


def test_stall_notice_card_formats_elapsed_and_current_action():
    card = format_stall_notice_card(
        elapsed_minutes=12,
        details=["iteration 8/90", "terminal"],
    )

    assert card == (
        "⏳ Still working — 12 min elapsed\n"
        "Status: iteration 8/90, terminal\n"
        "Next: Continuing automatically; use /stop if you want to cancel."
    )
