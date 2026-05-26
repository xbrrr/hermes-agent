from gateway.run import (
    _GATEWAY_MULTI_STEP_CODE_AS_ACTION_HINT,
    _append_gateway_code_as_action_hint,
)


def test_gateway_code_as_action_hint_contains_required_phrase_and_example():
    hint = _GATEWAY_MULTI_STEP_CODE_AS_ACTION_HINT
    assert "For multi-step tasks (3+ sequential tool calls)" in hint
    assert "execute_code with hermes_tools imports" in hint
    assert "from hermes_tools import" in hint


def test_gateway_code_as_action_hint_appends_idempotently():
    prompt = "existing context"
    once = _append_gateway_code_as_action_hint(prompt)
    twice = _append_gateway_code_as_action_hint(once)
    assert once == twice
    assert once.startswith(prompt)
    assert _GATEWAY_MULTI_STEP_CODE_AS_ACTION_HINT in once
