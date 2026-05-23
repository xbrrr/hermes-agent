# Local STT / whisper wrapper troubleshooting

Session-derived fix pattern for Hermes local voice transcription on macOS when using `whisper.cpp` wrappers.

## Symptom

Voice transcription reports a model-path error similar to:

```text
Local STT failed: whisper wrapper: model file not found.
Set WHISPER_CPP_MODEL=/path/to/ggml-model.bin or place a model in ~/.local/share/whisper/.
```

A common local model path on this Mac is:

```text
/Users/xbr/.local/share/whisper/ggml-base.bin
```

## Durable fix pattern

- Check whether the wrapper receives `--model base` / `--model small` / etc. and mistakenly treats the model name as a literal filesystem path.
- The wrapper should resolve known model names to `ggml-<name>.bin` candidates in the configured/local model directory.
- If `WHISPER_CPP_MODEL` is set, treat it as a preferred candidate without printing its environment context broadly.
- Smoke-test through the same CLI path Hermes uses, not only through a direct `whisper-cli` command.
- Prefer `hermes config set stt.local.language auto` if language forcing causes wrong-language transcription.
- This wrapper-level fix applies on the next transcription call and usually does not require a Hermes gateway restart.

## Pitfalls

- Do not encode this as “local STT is broken.” The lesson is wrapper model-name resolution and same-path smoke testing.
- Do not restart Hermes for a wrapper-only fix unless live runtime config actually requires reload.
- Do not print raw voice transcript contents in public ops summaries unless the user asked for it; summarize the operational result.
