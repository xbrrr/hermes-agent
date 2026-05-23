# Claude via OpenRouter from Hermes through VPS

Use this when Anthropic/Claude OAuth is authenticated but third-party inference is gated, or when the user wants Claude in Hermes without relying on Claude account OAuth limits.

## Recommended path

1. Keep Hermes gateway egress on the per-process VPS proxy (`HTTP_PROXY`/`HTTPS_PROXY`), not a global Tailscale exit node.
2. Have the user create an OpenRouter key in the dedicated VPS browser profile:
   - `https://openrouter.ai/settings/keys`
3. Have the user add credits:
   - `https://openrouter.ai/settings/credits`
4. Do not ask the user to paste the key into Telegram. Prefer local clipboard/file ingestion on the Mac and redact all output.
5. Store the key as `OPENROUTER_API_KEY` in Hermes env/config/credential storage, without printing the value.
6. Smoke with an explicit Claude model via OpenRouter, e.g.:
   - `--provider openrouter --model anthropic/claude-sonnet-4.5`

## Expected errors and interpretation

- `HTTP 402: Insufficient credits. This account never purchased credits.`
  - OpenRouter key is recognized and routing reached OpenRouter.
  - The fix is credits/billing on OpenRouter, not Hermes auth or VPS proxy.

- Claude OAuth error: `Third-party apps now draw from your extra usage...`
  - This is an Anthropic account/plan gating issue for third-party OAuth inference.
  - Do not assume a separate `extra usage` UI exists for every account; if the user says the UI only shows ordinary limits, stop insisting and switch to OpenRouter or Anthropic API key.

## User-facing style

For Mikhail during provider setup, answer as a short checklist:

- current status;
- exact URL he must open;
- exact human action needed;
- what Hermes will do after.

Avoid repeating long provider architecture unless asked.
