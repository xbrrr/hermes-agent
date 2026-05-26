"""Runtime model/fallback monitoring for long-lived agents.

The monitor is intentionally outside the provider retry loop: fallback still
does the urgent rescue, while this module logs the active runtime, notifies on
fallback activation, and probes the primary before allowing a turn to move
back from fallback.
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from dataclasses import dataclass
from typing import Any

from agent.error_classifier import FailoverReason, classify_api_error

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RuntimeMonitorConfig:
    enabled: bool = False
    probe_interval_seconds: float = 300.0
    probe_timeout_seconds: float = 20.0
    notify_cooldown_seconds: float = 900.0
    notify_platform: str = "telegram"
    notify_chat_id: str = ""
    notify_thread_id: str = ""


def _coerce_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    return default


def _coerce_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _load_monitor_config() -> RuntimeMonitorConfig:
    try:
        from hermes_cli.config import cfg_get, load_config_readonly

        cfg = load_config_readonly()
        raw = cfg_get(cfg, "runtime_model_monitor", default={})
    except Exception:
        raw = {}
    if not isinstance(raw, dict):
        raw = {}

    target = raw.get("target") if isinstance(raw.get("target"), dict) else {}
    return RuntimeMonitorConfig(
        enabled=_coerce_bool(raw.get("enabled"), False),
        probe_interval_seconds=max(30.0, _coerce_float(raw.get("probe_interval_seconds"), 300.0)),
        probe_timeout_seconds=max(3.0, _coerce_float(raw.get("probe_timeout_seconds"), 20.0)),
        notify_cooldown_seconds=max(0.0, _coerce_float(raw.get("notify_cooldown_seconds"), 900.0)),
        notify_platform=str(target.get("platform") or raw.get("notify_platform") or "telegram").strip().lower(),
        notify_chat_id=str(target.get("chat_id") or raw.get("notify_chat_id") or "").strip(),
        notify_thread_id=str(target.get("thread_id") or raw.get("notify_thread_id") or "").strip(),
    )


def monitor_enabled() -> bool:
    return _load_monitor_config().enabled


def _runtime_label(agent: Any) -> str:
    provider = (getattr(agent, "provider", "") or "unknown").strip()
    model = (getattr(agent, "model", "") or "unknown").strip()
    api_mode = (getattr(agent, "api_mode", "") or "unknown").strip()
    return f"{provider}/{model} api_mode={api_mode}"


def before_llm_call(agent: Any, *, call_site: str = "") -> None:
    """Log the active provider/model immediately before a provider call."""
    cfg = _load_monitor_config()
    if not cfg.enabled:
        return
    logger.info(
        "runtime_model_monitor: active runtime before LLM call: %s fallback_active=%s session=%s call_site=%s",
        _runtime_label(agent),
        bool(getattr(agent, "_fallback_activated", False)),
        getattr(agent, "session_id", "") or "",
        call_site or "unknown",
    )


def _reason_text(reason: Any) -> str:
    if isinstance(reason, FailoverReason):
        return reason.value
    if reason is None:
        return "unknown"
    return str(reason)


def _detail_text(detail: Any) -> str:
    text = str(detail or "").strip()
    if not text:
        return ""
    return text.replace("\n", " ")[:500]


def _notify_target(cfg: RuntimeMonitorConfig) -> str | None:
    if not cfg.notify_platform or not cfg.notify_chat_id:
        return None
    if cfg.notify_thread_id:
        return f"{cfg.notify_platform}:{cfg.notify_chat_id}:{cfg.notify_thread_id}"
    return f"{cfg.notify_platform}:{cfg.notify_chat_id}"


def _send_notification(cfg: RuntimeMonitorConfig, message: str, *, key: str = "") -> None:
    target = _notify_target(cfg)
    if not target:
        logger.info("runtime_model_monitor: notification skipped, no target configured: %s", message)
        return
    try:
        try:
            from hermes_cli.config import load_env

            for env_key, env_value in load_env().items():
                if env_key and env_value and env_key not in os.environ:
                    os.environ[env_key] = env_value
        except Exception:
            pass
        from tools.send_message_tool import send_message_tool

        result = send_message_tool({
            "action": "send",
            "target": target,
            "message": message,
        })
        try:
            parsed = json.loads(result) if isinstance(result, str) else result
        except Exception:
            parsed = result
        if isinstance(parsed, dict) and parsed.get("error"):
            logger.warning(
                "runtime_model_monitor: notification failed key=%s target=%s error=%s",
                key,
                target,
                parsed.get("error"),
            )
    except Exception as exc:
        logger.warning(
            "runtime_model_monitor: notification failed key=%s target=%s: %s",
            key,
            target,
            exc,
        )


def _notify_once(agent: Any, cfg: RuntimeMonitorConfig, key: str, message: str) -> None:
    now = time.monotonic()
    sent = getattr(agent, "_runtime_monitor_notify_sent_at", None)
    if not isinstance(sent, dict):
        sent = {}
        agent._runtime_monitor_notify_sent_at = sent
    last = float(sent.get(key, 0.0) or 0.0)
    if cfg.notify_cooldown_seconds and now - last < cfg.notify_cooldown_seconds:
        return
    sent[key] = now

    thread = threading.Thread(
        target=_send_notification,
        args=(cfg, message),
        kwargs={"key": key},
        name="runtime-model-monitor-notify",
        daemon=True,
    )
    thread.start()


def on_fallback_activated(
    agent: Any,
    *,
    reason: Any = None,
    reason_detail: Any = None,
    from_provider: str = "",
    from_model: str = "",
    to_provider: str = "",
    to_model: str = "",
) -> None:
    cfg = _load_monitor_config()
    if not cfg.enabled:
        return

    reason_label = _reason_text(reason)
    detail_label = _detail_text(reason_detail)
    agent._runtime_monitor_primary_healthy = False
    agent._runtime_monitor_last_failure_reason = (
        f"{reason_label}: {detail_label}" if detail_label else reason_label
    )
    agent._runtime_monitor_next_probe_at = time.monotonic() + cfg.probe_interval_seconds

    logger.warning(
        "runtime_model_monitor: fallback activated primary=%s/%s fallback=%s/%s reason=%s detail=%s session=%s",
        from_provider or ((getattr(agent, "_primary_runtime", {}) or {}).get("provider") or "unknown"),
        from_model or ((getattr(agent, "_primary_runtime", {}) or {}).get("model") or "unknown"),
        to_provider or getattr(agent, "provider", "") or "unknown",
        to_model or getattr(agent, "model", "") or "unknown",
        reason_label,
        detail_label or "-",
        getattr(agent, "session_id", "") or "",
    )

    # Dynamic notification for multi-level fallback chain
    from_label = f"{from_provider or 'anthropic'}/{from_model or ((getattr(agent, '_primary_runtime', {}) or {}).get('model') or 'unknown')}"
    to_label = f"{to_provider or getattr(agent, 'provider', 'unknown')}/{to_model or getattr(agent, 'model', 'unknown')}"
    
    _notify_once(
        agent,
        cfg,
        "fallback_red",
        (
            f"⚠️ **Provider fallback**: {from_label} → {to_label}\n"
            f"**Причина:** {reason_label}\n"
            + (f"**Деталь:** {detail_label}\n" if detail_label else "")
            + f"**Health-check:** каждые {int(cfg.probe_interval_seconds // 60) or 1} мин.\n"
            f"**Session:** {getattr(agent, 'session_id', '') or 'unknown'}"
        ),
    )
    _ensure_probe_thread(agent, cfg)


def can_restore_primary_runtime(agent: Any) -> bool:
    """Return True only after the primary passes a lightweight health probe."""
    cfg = _load_monitor_config()
    if not cfg.enabled:
        return True
    if not getattr(agent, "_fallback_activated", False):
        return True
    if bool(getattr(agent, "_runtime_monitor_primary_healthy", False)):
        agent._rate_limited_until = 0
        return True

    now = time.monotonic()
    next_probe_at = float(getattr(agent, "_runtime_monitor_next_probe_at", 0.0) or 0.0)
    if now < next_probe_at:
        logger.info(
            "runtime_model_monitor: primary restore deferred for %.0fs; current=%s",
            next_probe_at - now,
            _runtime_label(agent),
        )
        return False

    ok, detail = probe_primary(agent, cfg)
    if ok:
        _mark_primary_healthy(agent, cfg, detail=detail)
        agent._rate_limited_until = 0
        return True

    agent._runtime_monitor_primary_healthy = False
    agent._runtime_monitor_last_probe_error = detail
    agent._runtime_monitor_next_probe_at = now + cfg.probe_interval_seconds
    logger.warning("runtime_model_monitor: primary restore blocked, probe failed: %s", detail)
    _ensure_probe_thread(agent, cfg)
    return False


def _ensure_probe_thread(agent: Any, cfg: RuntimeMonitorConfig) -> None:
    existing = getattr(agent, "_runtime_monitor_probe_thread", None)
    if existing is not None and existing.is_alive():
        return
    thread = threading.Thread(
        target=_probe_loop,
        args=(agent,),
        name="runtime-model-monitor-probe",
        daemon=True,
    )
    agent._runtime_monitor_probe_thread = thread
    thread.start()


def _probe_loop(agent: Any) -> None:
    while True:
        cfg = _load_monitor_config()
        if not cfg.enabled or not getattr(agent, "_fallback_activated", False):
            return
        if bool(getattr(agent, "_runtime_monitor_primary_healthy", False)):
            return
        time.sleep(cfg.probe_interval_seconds)
        if not cfg.enabled or not getattr(agent, "_fallback_activated", False):
            return
        ok, detail = probe_primary(agent, cfg)
        if ok:
            _mark_primary_healthy(agent, cfg, detail=detail)
            return
        agent._runtime_monitor_last_probe_error = detail
        agent._runtime_monitor_next_probe_at = time.monotonic() + cfg.probe_interval_seconds
        logger.warning("runtime_model_monitor: background primary probe failed: %s", detail)


def _mark_primary_healthy(agent: Any, cfg: RuntimeMonitorConfig, *, detail: str = "") -> None:
    agent._runtime_monitor_primary_healthy = True
    agent._runtime_monitor_next_probe_at = 0.0
    logger.info("runtime_model_monitor: primary probe recovered: %s", detail)
    rt = getattr(agent, "_primary_runtime", {}) or {}
    _notify_once(
        agent,
        cfg,
        "primary_green",
        (
            "GREEN Sonnet восстановлен\n"
            f"Primary: {rt.get('provider') or 'anthropic'}/{rt.get('model') or 'unknown'}\n"
            "Следующий turn автоматически пойдёт через Sonnet; текущий turn не трогаю mid-flight."
        ),
    )


def probe_primary(agent: Any, cfg: RuntimeMonitorConfig | None = None) -> tuple[bool, str]:
    cfg = cfg or _load_monitor_config()
    rt = getattr(agent, "_primary_runtime", {}) or {}
    provider = str(rt.get("provider") or "").strip().lower()
    model = str(rt.get("model") or "").strip()
    api_mode = str(rt.get("api_mode") or "").strip()
    if not provider or not model:
        return False, "primary runtime snapshot is incomplete"

    try:
        if api_mode == "anthropic_messages" or provider == "anthropic":
            from agent.anthropic_adapter import build_anthropic_client

            api_key = rt.get("anthropic_api_key") or rt.get("api_key") or getattr(agent, "_anthropic_api_key", "")
            base_url = rt.get("anthropic_base_url") or rt.get("base_url") or None
            client = build_anthropic_client(api_key, base_url, timeout=cfg.probe_timeout_seconds)
            client.messages.create(
                model=model,
                max_tokens=1,
                messages=[{"role": "user", "content": "ping"}],
            )
            return True, f"{provider}/{model} probe ok"

        from agent.auxiliary_client import resolve_provider_client

        client, resolved_model = resolve_provider_client(provider, model=model, raw_codex=True)
        if client is None:
            return False, f"{provider}/{model} credentials unavailable"
        resolved_model = resolved_model or model
        if api_mode == "codex_responses" or provider == "openai-codex":
            client.responses.create(model=resolved_model, input="ping", max_output_tokens=1)
        else:
            client.chat.completions.create(
                model=resolved_model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=1,
            )
        return True, f"{provider}/{resolved_model} probe ok"
    except Exception as exc:  # noqa: BLE001 - probe must classify any provider SDK error.
        classified = classify_api_error(exc, provider=provider, model=model)
        return False, f"{classified.reason.value}: {classified.message or str(exc)}"


__all__ = [
    "before_llm_call",
    "can_restore_primary_runtime",
    "monitor_enabled",
    "on_fallback_activated",
    "probe_primary",
]
