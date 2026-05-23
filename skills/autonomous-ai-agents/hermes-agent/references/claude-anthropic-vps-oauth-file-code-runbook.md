# Claude/Anthropic VPS OAuth runbook

Use this when connecting a Claude Pro/Max account to Hermes via Anthropic OAuth while keeping account setup and OAuth authorization on a dedicated VPS/proxy browser profile.

## Context

Mikhail's preferred flow for Claude/Anthropic is analogous to ChatGPT Codex: OAuth/subscription-style auth when possible, not a regular Anthropic API key unless explicitly chosen. For region-sensitive setup, keep browser signup/payment/OAuth and Hermes provider traffic on the same Finnish VPS route.

## Key pitfall

Do **not** rely on `hermes auth add anthropic --type oauth --no-browser` as the only guard in Hermes versions where the Anthropic PKCE helper ignores the CLI `--no-browser` flag and calls `webbrowser.open()` directly. That can open the OAuth URL in the default browser/profile.

Safer options:

1. Patch Hermes so Anthropic auth receives and honors an `open_browser` / `no_browser` flag.
2. Or set a temporary `BROWSER` wrapper that launches the dedicated VPS Chrome profile.

## VPS Chrome wrapper

Use a wrapper like:

```zsh
#!/bin/zsh
set -euo pipefail
CHROME_APP="/Applications/Google Chrome.app"
PROFILE_DIR="$HOME/.chrome-vps-profile"
PROXY_URL="http://100.100.1.1:18080"
URL="${1:-https://claude.ai}"
mkdir -p "$PROFILE_DIR"
exec /usr/bin/open -na "$CHROME_APP" --args \
  --user-data-dir="$PROFILE_DIR" \
  --proxy-server="$PROXY_URL" \
  --proxy-bypass-list="<-loopback>" \
  --host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE 100.100.1.1" \
  --disable-quic \
  --no-first-run \
  "$URL"
```

Then run OAuth with:

```bash
cd /Users/xbr/.local/src/hermes-agent
BROWSER=/tmp/hermes-open-chrome-vps-url.sh .venv/bin/hermes auth add anthropic --type oauth --label claude-vps
```

## Handling the authentication code

Prefer not to paste the OAuth code in Telegram. Safer options:

- User copies the code to clipboard on the Mac mini; agent reads clipboard locally.
- User saves the code in a local temporary file (for example `~/Desktop/1.rtf` or `~/Desktop/1.txt`); agent extracts it locally and submits to the waiting process.

If using a file, ensure the code matches the currently active OAuth URL/state. If the OAuth process restarts, the previous code becomes invalid and the user must authorize the newly opened URL and overwrite the file with the new code.

For `.rtf`, extract plaintext with:

```bash
/usr/bin/textutil -convert txt -stdout "$HOME/Desktop/1.rtf"
```

Avoid logging or printing the code. Report only length/status, never the value.

## Common failure mode

`Token exchange failed: HTTP Error 400: Bad Request` usually means:

- the code was copied from a previous OAuth state;
- the code was partially copied;
- a literal shell substitution string such as `$(cat /tmp/code)` was sent to an interactive process instead of the file contents.

Recovery:

1. Kill the failed OAuth process.
2. Start a fresh OAuth flow through the VPS browser wrapper.
3. Ask the user to authorize the newly opened page and update the local code file.
4. Submit the fresh code without printing it.

## Style note for Telegram

When Mikhail asks “короче”, answer as a short checklist with only the immediate human action and the next agent action. Avoid long explanations unless asked.
