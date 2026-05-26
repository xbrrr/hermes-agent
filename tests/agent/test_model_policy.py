import pytest

from agent.model_policy import (
    ForbiddenModelError,
    enforce_allowed_model,
    enforce_allowed_provider,
    is_forbidden_model,
    reject_forbidden_model,
)


def test_forbidden_models_match_env_patterns(monkeypatch):
    monkeypatch.setenv(
        "HERMES_FORBIDDEN_MODELS",
        "claude-haiku*, anthropic.claude-haiku*, claude-3-5-haiku*",
    )

    assert is_forbidden_model("claude-haiku-4-5-20251001")
    assert is_forbidden_model("anthropic/claude-haiku-4-5-20251001")
    assert is_forbidden_model("anthropic.claude-haiku-4-5-20251001-v1:0")
    assert is_forbidden_model("claude-3-5-haiku-20241022")
    assert not is_forbidden_model("claude-sonnet-4-5-20250929")
    assert not is_forbidden_model("gpt-5.5")


def test_enforce_allowed_model_raises_for_forbidden_model(monkeypatch):
    monkeypatch.setenv("HERMES_FORBIDDEN_MODELS", "claude-haiku*")

    with pytest.raises(ForbiddenModelError):
        enforce_allowed_model("claude-haiku-4-5-20251001", usage="main")


def test_reject_forbidden_model_returns_boolean(monkeypatch):
    monkeypatch.setenv("HERMES_FORBIDDEN_MODELS", "claude-haiku*")

    assert reject_forbidden_model("claude-haiku-4-5-20251001", usage="aux")
    assert not reject_forbidden_model("claude-sonnet-4-5-20250929", usage="aux")


def test_auxiliary_resolver_rejects_forbidden_explicit_model(monkeypatch):
    monkeypatch.setenv("HERMES_FORBIDDEN_MODELS", "claude-haiku*")

    from agent.auxiliary_client import resolve_provider_client

    client, model = resolve_provider_client(
        "anthropic",
        "claude-haiku-4-5-20251001",
        explicit_api_key="test-token",
    )

    assert client is None
    assert model is None


def test_allowed_provider_policy_rejects_unlisted_provider(monkeypatch):
    monkeypatch.setenv("HERMES_ALLOWED_PROVIDERS", "anthropic,openai-codex")

    assert enforce_allowed_provider("anthropic", usage="main") == "anthropic"
    assert enforce_allowed_provider("openai-codex", usage="fallback") == "openai-codex"

    with pytest.raises(ForbiddenModelError):
        enforce_allowed_provider("openrouter", usage="fallback")
