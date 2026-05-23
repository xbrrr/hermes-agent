# Claude/Anthropic auth provider triage for Hermes

Use this when setting up Claude in Hermes and the user may have several paths available: Anthropic OAuth / Claude subscription, Anthropic Console API key, and OpenRouter.

## Principles

- Keep the paths separate in both testing and reporting:
  - **Anthropic OAuth / Claude subscription**: credential-pool OAuth entry, Bearer auth, subscription/third-party limits.
  - **Anthropic Console API key**: `ANTHROPIC_API_KEY`, x-api-key auth, separate Anthropic API billing.
  - **OpenRouter**: `OPENROUTER_API_KEY`, OpenRouter balance and model IDs, separate billing.
- Do not switch Hermes default model/provider, restart the gateway, or route production Telegram traffic to a newly-added provider unless the user explicitly asks.
- Do smoke tests with the exact auth path under test. If the user asks to test OAuth, do not let `ANTHROPIC_API_KEY` accidentally satisfy the request.
- Never paste secrets into Telegram or logs. Prefer clipboard/local file ingestion and redact outputs.

## OAuth via VPS Chrome profile

When Claude/Anthropic login must happen through a VPS/browser profile:

- Use the dedicated Chrome profile and proxy, e.g. `--user-data-dir=$HOME/.chrome-vps-profile` and `--proxy-server=http://100.100.1.1:18080`.
- Do not assume `hermes auth add anthropic --type oauth --no-browser` prevents browser opening in all Hermes versions; the Anthropic helper may call `webbrowser.open()` directly.
- If needed, set `BROWSER` to a wrapper that opens URLs in the VPS Chrome profile.
- OAuth authorization codes are state-bound. If the auth process restarts or the wrong text is submitted, open the newly generated URL and obtain a fresh code.
- If the user gives the code via clipboard/file, read it locally and do not echo it. For RTF files, extract plaintext with `textutil -convert txt -stdout`.

## OAuth-only smoke pattern

Do not use `hermes chat --provider anthropic` to prove OAuth if an API key is present, because runtime resolution may prefer env/config credentials. Instead, load the OAuth entry from the credential pool and build the Anthropic client with that access token:

```python
from agent.credential_pool import load_pool, AUTH_TYPE_OAUTH
from agent.anthropic_adapter import build_anthropic_client, refresh_anthropic_oauth_pure, _is_oauth_token

pool = load_pool('anthropic')
entry = next(e for e in pool.entries() if e.auth_type == AUTH_TYPE_OAUTH or e.label == 'claude-vps')
access = (entry.access_token or '').strip()
refresh = (entry.refresh_token or '').strip()
# Refresh transiently if nearly expired, without printing tokens.
client = build_anthropic_client(access, base_url='https://api.anthropic.com', timeout=60)
msg = client.messages.create(
    model='claude-sonnet-4-5-20250929',
    max_tokens=16,
    messages=[{'role': 'user', 'content': 'Reply exactly: OAUTH_SMOKE_OK'}],
)
```

Report concise state:

- OAuth credential present / missing.
- Refresh token present / missing.
- Access token lifetime if available.
- Exact provider error class/status, redacted request id.

Interpretation examples:

- `400` with `Third-party apps now draw from your extra usage...`: OAuth works, but Anthropic account/plan gates third-party usage. Do not assert the UI must expose an `extra usage` control; the UI may show only ordinary limits.
- `429 rate_limit_error`: OAuth works and request reached Anthropic, but account/third-party usage is rate-limited or temporarily capped.
- `401`: token expired/revoked or refresh path failed; try refresh, then redo OAuth if needed.

## Console API key setup

- If the user provides an Anthropic API key, validate shape/suffix without printing it.
- Store in `~/.hermes/.env` as `ANTHROPIC_API_KEY=...` and/or `hermes auth add anthropic --type api-key`; back up `.env` first.
- Smoke explicitly with the API-key path and redaction.
- Clean clipboard and temporary files after ingesting the key.
- Still do not make this the default provider unless the user asks.

## OpenRouter path

- Check for `OPENROUTER_API_KEY` and smoke with an OpenRouter Claude model.
- If OpenRouter returns `402 Insufficient credits`, the key is recognized but the account/balance is not funded.
- OpenRouter billing and model IDs are separate from Anthropic OAuth/API billing.

## User-facing style for this workflow

For Mikhail, keep Telegram reports short: current status, exact blocker/error, what he must do next. Avoid long provider background unless asked.