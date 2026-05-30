"""Regression test for #17929: AIAgent.__init__ should try fallback_model
when primary provider credentials are exhausted."""
import pytest
from unittest.mock import patch, MagicMock
from run_agent import AIAgent


def _make_tool_defs():
    return [{"type": "function", "function": {"name": "web_search",
             "description": "search", "parameters": {"type": "object", "properties": {}}}}]


def _mock_client(api_key="fb-key-1234567890", base_url="https://fb.example.com/v1"):
    c = MagicMock()
    c.api_key = api_key
    c.base_url = base_url
    c._default_headers = None
    return c


def test_init_tries_fallback_when_primary_returns_none():
    """When resolve_provider_client returns None for primary but succeeds for
    a fallback entry, __init__ should NOT raise RuntimeError."""
    fb = _mock_client()

    def fake_resolve(provider, model=None, raw_codex=False,
                     explicit_base_url=None, explicit_api_key=None, **kwargs):
        if provider == "tencent-token-plan":
            return fb, "kimi2.5"
        return None, None  # primary exhausted

    with patch("agent.auxiliary_client.resolve_provider_client", side_effect=fake_resolve), \
         patch("run_agent.get_tool_definitions", return_value=_make_tool_defs()), \
         patch("run_agent.check_toolset_requirements", return_value={}), \
         patch("run_agent.OpenAI", return_value=MagicMock()):

        agent = AIAgent(
            provider="alibaba-coding-plan",
            model="qwen3.6-plus",
            api_key=None,
            base_url=None,
            quiet_mode=True,
            skip_context_files=True,
            skip_memory=True,
            fallback_model=[{"provider": "tencent-token-plan", "model": "kimi2.5"}],
        )
        assert agent.provider == "tencent-token-plan"
        assert agent.model == "kimi2.5"
        assert agent._fallback_activated is True


def test_init_fallback_preserves_anthropic_wrapper_transport():
    """Init-time fallback must not rebuild an Anthropic wrapper as OpenAI-wire."""
    from agent.auxiliary_client import AnthropicAuxiliaryClient

    real_anthropic_client = MagicMock()
    fb = AnthropicAuxiliaryClient(
        real_anthropic_client,
        "claude-sonnet-4-6",
        "meridian-local-key",
        "http://127.0.0.1:3456",
        is_oauth=False,
    )

    def fake_resolve(provider, model=None, raw_codex=False, **kwargs):
        if provider == "custom:meridian-claude-max":
            assert kwargs.get("api_mode") == "anthropic_messages"
            return fb, "claude-sonnet-4-6"
        return None, None  # primary exhausted

    with patch("agent.auxiliary_client.resolve_provider_client", side_effect=fake_resolve), \
         patch("run_agent.get_tool_definitions", return_value=_make_tool_defs()), \
         patch("run_agent.check_toolset_requirements", return_value={}), \
         patch("run_agent.OpenAI", return_value=MagicMock()) as mock_openai:

        agent = AIAgent(
            provider="alibaba-coding-plan",
            model="qwen3.6-plus",
            api_key=None,
            base_url=None,
            quiet_mode=True,
            skip_context_files=True,
            skip_memory=True,
            fallback_model=[
                {
                    "provider": "custom:meridian-claude-max",
                    "model": "claude-sonnet-4-6",
                    "api_mode": "anthropic_messages",
                }
            ],
        )

    assert agent.provider == "custom:meridian-claude-max"
    assert agent.model == "claude-sonnet-4-6"
    assert agent.base_url == "http://127.0.0.1:3456"
    assert agent.api_key == "meridian-local-key"
    assert agent.api_mode == "anthropic_messages"
    assert agent.client is None
    assert agent._anthropic_client is real_anthropic_client
    mock_openai.assert_not_called()


def test_init_primary_router_preserves_anthropic_wrapper_transport():
    from agent.auxiliary_client import AnthropicAuxiliaryClient

    real_anthropic_client = MagicMock()
    routed = AnthropicAuxiliaryClient(
        real_anthropic_client,
        "claude-sonnet-4-6",
        "meridian-local-key",
        "http://127.0.0.1:3456",
        is_oauth=False,
    )

    with patch("agent.auxiliary_client.resolve_provider_client", return_value=(routed, "claude-sonnet-4-6")), \
         patch("run_agent.get_tool_definitions", return_value=_make_tool_defs()), \
         patch("run_agent.check_toolset_requirements", return_value={}), \
         patch("run_agent.OpenAI", return_value=MagicMock()) as mock_openai:

        agent = AIAgent(
            provider="custom:meridian-claude-max",
            model="claude-sonnet-4-6",
            api_key=None,
            base_url=None,
            quiet_mode=True,
            skip_context_files=True,
            skip_memory=True,
        )

    assert agent.api_mode == "anthropic_messages"
    assert agent.client is None
    assert agent._anthropic_client is real_anthropic_client
    mock_openai.assert_not_called()


def test_init_raises_when_no_fallback_configured():
    """When primary returns None and no fallback is set, should raise."""
    with patch("agent.auxiliary_client.resolve_provider_client", return_value=(None, None)), \
         patch("run_agent.get_tool_definitions", return_value=_make_tool_defs()), \
         patch("run_agent.check_toolset_requirements", return_value={}), \
         patch("run_agent.OpenAI", return_value=MagicMock()):

        with pytest.raises(RuntimeError, match="no API key was found"):
            AIAgent(
                provider="alibaba-coding-plan",
                model="qwen3.6-plus",
                api_key=None,
                base_url=None,
                quiet_mode=True,
                skip_context_files=True,
                skip_memory=True,
                fallback_model=None,
            )
