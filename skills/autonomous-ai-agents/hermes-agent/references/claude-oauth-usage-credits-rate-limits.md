# Claude OAuth usage credits and Sonnet/Haiku rate-limit triage

Use this when configuring Hermes Anthropic/Claude OAuth (`hermes auth add anthropic --type oauth`) and the user has Claude usage credits enabled.

## Key distinction

Anthropic OAuth can be healthy even when a specific model returns `429 rate_limit_error`.

Observed production-shaped pattern:

- OAuth credential exists and has an access token + refresh token.
- The access token can still be valid for hours.
- `claude-haiku-4-5-20251001` succeeds through the same OAuth credential.
- Sonnet models such as `claude-sonnet-4-20250514` and `claude-sonnet-4-5-20250929` return `429 rate_limit_error`.
- This means auth and usage credits are working in principle; the limiter is likely model-class / plan / session / acceleration related, not a missing balance or broken proxy.

Do not tell the user to buy/add credits again if the UI already shows credits and Haiku works. Report the exact per-model result.

## What 429 can mean

Anthropic docs describe 429 as rate limiting, not a single condition. It may be triggered by:

- RPM: requests per minute.
- ITPM: input tokens per minute.
- OTPM: output tokens per minute.
- Acceleration limits: sharp increase in usage after a new account, new credential, or newly enabled credits.
- Claude plan/session/weekly/model-class limits.
- Heavy model class limits: Sonnet/Opus can be limited when Haiku is still available.

If response headers include `x-should-retry: true` but no useful `retry-after`, treat it as an internal/windowed/model-class limiter. Avoid manual hammering; retry gently later.

## Verification pattern without using API key

When the user asks to test OAuth only and an `ANTHROPIC_API_KEY` is also configured, do not run a normal `hermes chat --provider anthropic` smoke unless you have verified it selects the OAuth credential. Prefer a small Python probe that:

1. Loads `load_pool('anthropic')`.
2. Selects the credential whose `auth_type` is OAuth or label is the intended OAuth label (e.g. `claude-vps`).
3. Builds the Anthropic client directly with that OAuth access token via `build_anthropic_client(token, base_url='https://api.anthropic.com')`.
4. Tests multiple models with tiny prompts and `max_tokens` <= 16.
5. Redacts tokens/request ids from output.

Expected concise output shape:

```text
OAUTH_STATUS present label=claude-vps token_is_oauth=True refresh_token_present=True expires_in_s=...
claude-haiku-4-5-20251001 OK OK
claude-sonnet-4-20250514 ERR RateLimitError ...
claude-sonnet-4-5-20250929 ERR RateLimitError ...
```

If `Haiku OK` and `Sonnet 429`, say: OAuth and credits work; Sonnet is currently model-limited. Do not call it an auth/proxy failure.

## Operational recommendation

- Use Haiku OAuth for lightweight Hermes work while Sonnet is limited.
- Retry Sonnet gently every 30-60 minutes, or after the user's Claude session/weekly usage reset.
- Do not spam Sonnet probes; that can extend acceleration/rate windows.
- Keep Anthropic API key as an explicit opt-in emergency path for Sonnet. If the user says not to use API key, do not use it in smoke tests or default routing.

## Haiku vs Sonnet positioning

Haiku 4.5 is suitable for:

- fast Telegram answers;
- classification/routing;
- summaries and rewrites;
- translations;
- simple log inspection;
- lightweight code review;
- small scripts;
- cheap/frequent cron/watchdog checks.

Sonnet is preferred for:

- complex reasoning;
- substantial coding/refactors;
- architecture/debugging;
- large context work;
- autonomous coding loops;
- higher-stakes review.

User-facing framing for Mikhail: keep it short. “OAuth работает, credits работают, Haiku доступен; Sonnet сейчас режется 429 по классу модели/лимиту, стоит ждать и мягко ретраить, API key не трогаю без команды.”
