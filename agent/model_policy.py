"""Runtime model policy checks.

This module is intentionally small and dependency-light: it is imported by
main-agent and auxiliary routing paths, so policy violations are caught before
an unwanted model can be used for a user turn, fallback, or compression task.
"""

from __future__ import annotations

import fnmatch
import logging
import os
from typing import Iterable, List

logger = logging.getLogger(__name__)


class ForbiddenModelError(RuntimeError):
    """Raised when runtime policy blocks a model."""


def _coerce_patterns(value) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        raw_items = value.replace("\n", ",").split(",")
    elif isinstance(value, Iterable):
        raw_items = [str(item) for item in value]
    else:
        raw_items = [str(value)]
    return [item.strip().lower() for item in raw_items if item and item.strip()]


def forbidden_model_patterns() -> List[str]:
    """Return configured forbidden model patterns.

    Sources:
    - HERMES_FORBIDDEN_MODELS, comma/newline separated.
    - config.yaml model.forbidden_models, list or comma-separated string.

    Patterns use fnmatch syntax and are case-insensitive.
    """

    patterns: List[str] = []
    patterns.extend(_coerce_patterns(os.getenv("HERMES_FORBIDDEN_MODELS")))

    try:
        from hermes_cli.config import load_config

        cfg = load_config()
        model_cfg = cfg.get("model") if isinstance(cfg, dict) else None
        if isinstance(model_cfg, dict):
            patterns.extend(_coerce_patterns(model_cfg.get("forbidden_models")))
    except Exception as exc:
        logger.debug("Could not read model.forbidden_models policy: %s", exc)

    return list(dict.fromkeys(patterns))


def allowed_provider_patterns() -> List[str]:
    """Return configured provider allow-list patterns.

    Empty means no provider allow-list is active.
    """

    patterns: List[str] = []
    patterns.extend(_coerce_patterns(os.getenv("HERMES_ALLOWED_PROVIDERS")))

    try:
        from hermes_cli.config import load_config

        cfg = load_config()
        model_cfg = cfg.get("model") if isinstance(cfg, dict) else None
        if isinstance(model_cfg, dict):
            patterns.extend(_coerce_patterns(model_cfg.get("allowed_providers")))
    except Exception as exc:
        logger.debug("Could not read model.allowed_providers policy: %s", exc)

    return list(dict.fromkeys(patterns))


def _model_candidates(model: str) -> List[str]:
    normalized = (model or "").strip().lower()
    if not normalized:
        return []
    candidates = [normalized]
    if "/" in normalized:
        candidates.append(normalized.rsplit("/", 1)[-1])
    return list(dict.fromkeys(candidates))


def is_forbidden_model(model: str) -> bool:
    candidates = _model_candidates(model)
    if not candidates:
        return False
    for pattern in forbidden_model_patterns():
        for candidate in candidates:
            if fnmatch.fnmatchcase(candidate, pattern):
                return True
    return False


def enforce_allowed_model(model: str, *, usage: str = "model") -> str:
    """Return *model* or raise when policy forbids it."""

    if is_forbidden_model(model):
        raise ForbiddenModelError(
            f"Model '{model}' is forbidden by runtime policy for {usage}."
        )
    return model


def is_allowed_provider(provider: str) -> bool:
    normalized = (provider or "").strip().lower()
    if not normalized:
        return True
    patterns = allowed_provider_patterns()
    if not patterns:
        return True
    return any(fnmatch.fnmatchcase(normalized, pattern) for pattern in patterns)


def enforce_allowed_provider(provider: str, *, usage: str = "provider") -> str:
    if not is_allowed_provider(provider):
        raise ForbiddenModelError(
            f"Provider '{provider}' is not allowed by runtime policy for {usage}."
        )
    return provider


def reject_forbidden_model(model: str, *, usage: str = "model") -> bool:
    """Log and return True when *model* is forbidden.

    Use in optional/fallback paths where returning no client is safer than
    raising and breaking the whole request.
    """

    if not is_forbidden_model(model):
        return False
    logger.warning(
        "Model %s is forbidden by runtime policy for %s; skipping",
        model,
        usage,
    )
    return True


def reject_forbidden_provider(provider: str, *, usage: str = "provider") -> bool:
    if is_allowed_provider(provider):
        return False
    logger.warning(
        "Provider %s is not allowed by runtime policy for %s; skipping",
        provider,
        usage,
    )
    return True
