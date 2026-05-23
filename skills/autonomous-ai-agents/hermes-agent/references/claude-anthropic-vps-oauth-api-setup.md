# Claude/Anthropic via VPS: OAuth, API key, OpenRouter runbook

Use this when setting up Claude/Anthropic for Hermes on the Mac mini with the Finnish VPS proxy.

## User-facing style

If Mikhail asks for brevity (e.g. `давай короче`), switch to a minimal checklist: what he must do now, what Hermes will do next, and one critical warning. Do not repeat architecture/background unless asked.

## Network invariant

- Keep global Tailscale exit node off unless explicitly requested.
- Use per-process proxy for Hermes/gateway/provider calls:
  - `HTTP_PROXY=http://100.100.1.1:18080`
  - `HTTPS_PROXY=http://100.100.1.1:18080`
  - lowercase variants too.
- Use the dedicated Chrome profile for account/payment/OAuth:
  - `--user-data-dir=$HOME/.chrome-vps-profile`
  - `--proxy-server=http://100.100.1.1:18080`
  - `--host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE 100.100.1.1"`
  - `--disable-quic`
- Verify direct vs proxied egress when needed, but report only concise status.

## Anthropic OAuth gotchas

- In the current Hermes Anthropic PKCE path, `--no-browser` may not be honored because the helper can call `webbrowser.open()` directly.
- Safer approach: run with `BROWSER=/path/to/vps-chrome-wrapper` where the wrapper launches Chrome with the VPS profile and proxy flags.
- If the user gives the authorization code via local file/clipboard, keep it out of Telegram and logs.
- OAuth authorization codes are state-bound. If the OAuth process restarts or the wrong text is submitted, open a fresh URL and require a fresh code from that new URL.
- If OAuth smoke returns `Third-party apps now draw from your extra usage...`, treat it as Anthropic account/plan gating, not proxy/auth failure. The UI may not expose a separate `extra usage` control; report the exact API error and offer API key/OpenRouter alternatives.

## Anthropic API key path

Best fallback when OAuth is gated:

1. User creates a key in Anthropic Console: `https://console.anthropic.com/settings/keys`.
2. User places it in Mac mini clipboard or a local file; do not ask them to paste it into Telegram.
3. Read it locally, validate expected shape/suffix if user provided one, but never print the key.
4. Backup `~/.hermes/.env` before editing.
5. Store as `ANTHROPIC_API_KEY=...` in `~/.hermes/.env` with mode `0600`.
6. Prefer also ensuring Hermes credential pool can see it; `hermes auth list anthropic` should show an env/API key entry without revealing the value.
7. Smoke with proxy env explicitly set, e.g. provider `anthropic`, model `claude-sonnet-4-5-20250929`, prompt requiring exact short output.
8. Clear clipboard and remove temporary key/code helper files.

Example smoke pattern, redacting output:

```bash
cd /Users/xbr/.local/src/hermes-agent
HTTP_PROXY=http://100.100.1.1:18080 \
HTTPS_PROXY=http://100.100.1.1:18080 \
http_proxy=http://100.100.1.1:18080 \
https_proxy=http://100.100.1.1:18080 \
.venv/bin/hermes chat -Q --provider anthropic \
  --model claude-sonnet-4-5-20250929 \
  -q 'Reply with exactly: ANTHROPIC_API_OK'
```

Expected success: `ANTHROPIC_API_OK`.

## OpenRouter alternative

- OpenRouter is separate billing and a separate API key (`OPENROUTER_API_KEY`).
- If smoke returns `HTTP 402: Insufficient credits`, the key is valid enough to reach OpenRouter but the account needs credits; it is not a Hermes proxy/auth bug.
- Use OpenRouter as a simple Claude provider path when Anthropic OAuth is gated, but only after the user funds OpenRouter.
