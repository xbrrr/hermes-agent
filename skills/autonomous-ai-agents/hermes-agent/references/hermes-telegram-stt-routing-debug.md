# Hermes Telegram STT + routing debug notes

Use this reference when Telegram voice transcription fails or the user asks whether Telegram topic routing gates are pre-LLM or post-LLM.

## Local STT failure: `whisper wrapper: model file not found`

Observed durable pattern on macOS Hermes installs using `whisper.cpp` through `~/.local/bin/whisper`:

- `tools.transcription_tools` auto-detects a local command and may invoke it like:
  - `whisper {input_path} --model base --output_format txt --output_dir {output_dir} --language {language}`
- A compatibility wrapper that expects `--model` to be a file path can incorrectly treat `base` as a missing file and ignore an otherwise valid `WHISPER_CPP_MODEL`.
- Fix the wrapper so model *names* (`tiny`, `base`, `small`, `medium`, `large-v3`, plus `.en` variants) resolve to GGML files such as `~/.local/share/whisper/ggml-base.bin` before erroring.
- Also verify `stt.local.language`; empty language can default to English in the wrapper pipeline and cause Russian voice to be translated/summarized into English. Set `auto` or an explicit language as appropriate:
  - `hermes config set stt.local.language auto`
  - or `hermes config set stt.local.language ru`

Minimal smoke:

```bash
bash -n ~/.local/bin/whisper
hermes config check
cd ~/.local/src/hermes-agent
.venv/bin/python - <<'PY'
from tools.transcription_tools import transcribe_audio
p = '/path/to/cached/audio.ogg'
r = transcribe_audio(p)
print(r.get('success'), r.get('provider'), r.get('error'))
print(r.get('transcript', '')[:1200])
PY
```

Manual recovery for a cached voice when gateway STT failed:

```bash
ffmpeg -y -i "$ogg" -ar 16000 -ac 1 -c:a pcm_s16le /tmp/hermes_voice.wav
whisper-cli -m "$WHISPER_CPP_MODEL" -f /tmp/hermes_voice.wav -l auto -otxt -of /tmp/hermes_voice
cat /tmp/hermes_voice.txt
```

## Telegram routing/wake path: pre-LLM vs post-LLM

For Hermes Telegram adapter (`gateway/platforms/telegram.py`), topic wake rules are pre-LLM gates. The usual text/command path is:

1. `_agentic_stack_observe_message(...)` records/passively observes scoped messages.
2. `_agentic_stack_should_suppress_hermes(decision)` can return before processing when another agent is explicitly intended.
3. `_should_process_message(...)` applies group/topic trigger rules.
4. Only after that does Hermes build a `MessageEvent`, clean bot trigger text, enqueue/handle it, and run the agent/LLM.

Inside `_should_process_message`, the effective order is:

1. DM/non-group: allow.
2. Ignored thread: deny.
3. Guest explicit mention bypass.
4. `allowed_chats` hard gate.
5. `free_response_chats`: allow.
6. `free_response_topics`: allow for `(chat_id, thread_id)`.
7. `require_mention=false`: allow.
8. Reply-to-bot: allow.
9. Explicit bot mention: allow.
10. Regex wake pattern: final allow/deny.

So `free_response_topics` bypasses the mention requirement for that chat/topic before LLM work starts; it is not a post-generation suppression rule.

## Interrupt/concurrency pitfall

If the user sees “Hermes starts answering and then cancels,” do not blame `free_response_topics` without checking logs. A common cause is `HERMES_GATEWAY_BUSY_INPUT_MODE=interrupt`: a new inbound update can interrupt an already-running API call, spending tokens before cancellation. That is separate from pre-LLM routing gates.

Evidence to collect:

```bash
grep -n "interrupted_during_api_call\|busy_input\|Flushing text batch\|_should_process_message\|soft routing suppressed\|Local STT command failed" ~/.hermes/logs/agent.log | tail -80
```

If the undesired turn already entered `run_agent: conversation turn`, routing has already allowed it or a separate in-flight turn was interrupted; inspect thread/topic, reply target, explicit mentions, and busy-input mode separately.
