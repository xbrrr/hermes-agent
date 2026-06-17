"""Small messaging UX cards for gateway control/status notices.

These helpers are intentionally presentation-only. They do not read config,
routing state, provider state, or mutate runtime behavior; gateway callers pass
already-computed facts and receive short text suitable for Telegram/Discord/etc.
"""

from __future__ import annotations

from typing import Iterable, Optional


def _clean_parts(parts: Iterable[object]) -> list[str]:
    return [str(part).strip() for part in parts if str(part or "").strip()]


def format_mm_control_card(
    *,
    state: str,
    action: str,
    details: Optional[Iterable[object]] = None,
    next_action: Optional[str] = None,
    blocker: Optional[str] = None,
) -> str:
    """Render a compact MM/gateway control card.

    The card keeps the old status meaning but makes chat UX scannable: state,
    optional current facts, next action, and blocker if present.
    """
    lines = [f"{state.strip()} — {action.strip()}" if action.strip() else state.strip()]
    detail_parts = _clean_parts(details or [])
    if detail_parts:
        lines.append("Status: " + ", ".join(detail_parts))
    if next_action and next_action.strip():
        lines.append("Next: " + next_action.strip())
    if blocker and blocker.strip():
        lines.append("Blocker: " + blocker.strip())
    return "\n".join(lines)


def format_busy_ack_card(
    *,
    mode: str,
    details: Optional[Iterable[object]] = None,
    demoted_for_subagents: bool = False,
) -> str:
    """Render the gateway's busy follow-up acknowledgement."""
    normalized = (mode or "interrupt").strip().lower()
    if normalized == "steer":
        return format_mm_control_card(
            state="⏩ Steered into current run",
            action="accepted",
            details=details,
            next_action="Your message arrives after the next tool call.",
        )
    if normalized == "queue" and demoted_for_subagents:
        return format_mm_control_card(
            state="⏳ Subagent working",
            action="queued",
            details=details,
            next_action="I will continue when it finishes; use /stop to cancel everything.",
        )
    if normalized == "queue":
        return format_mm_control_card(
            state="⏳ Current task running",
            action="queued",
            details=details,
            next_action="I will respond once the current task finishes.",
        )
    return format_mm_control_card(
        state="⚡ Current task interrupted",
        action="switching",
        details=details,
        next_action="I will respond to your message shortly.",
    )


def format_stall_notice_card(
    *,
    elapsed_minutes: int,
    details: Optional[Iterable[object]] = None,
) -> str:
    """Render a long-running/stall notice for messaging platforms."""
    return format_mm_control_card(
        state="⏳ Still working",
        action=f"{max(0, int(elapsed_minutes))} min elapsed",
        details=details,
        next_action="Continuing automatically; use /stop if you want to cancel.",
    )
