# Telegram agent non-response triage: Hermes/MM + OpenClaw/Bud

Use when a Telegram bot agent appears to stop responding, especially in Agentic Stack topics where Hermes/MM and OpenClaw/Bud coordinate.

## Key lesson

Do not assume the bot process is dead. In the 2026-05-19 Mac mini incident, both Hermes and OpenClaw were alive, but Telegram polling/ingress degraded:

- Hermes had `httpx.ProxyError: 502 Bad Gateway` and `Timed out` around the user-visible gap, then logged `Telegram polling resumed`.
- OpenClaw/Bud had repeated `fetch timeout ... api.telegram.org/.../getMe`, a `stale-socket` health-monitor restart, then isolated polling restarted and messages flowed again.
- Separately, Hermes responses were slowed by auxiliary/session-search/compression timeouts and unhealthy auxiliary providers, which is a tooling/runtime slowdown, not a host CPU outage.

## Fast evidence checklist

1. Baseline host/runtime without changing state:
   - `date`, `uptime`
   - `launchctl list | egrep 'hermes|openclaw|telegram|iq5000|ceo5000'`
   - `ps aux | egrep 'hermes|openclaw|gateway|codex'`
   - `lsof -nP -iTCP -sTCP:LISTEN | egrep 'node|python|hermes|openclaw'`

2. Verify service liveness:
   - `hermes gateway status`
   - OpenClaw local health endpoint if available, e.g. `curl -fsS http://127.0.0.1:<port>/health`
   - Telegram API reachability from host: repeated short probes to `https://api.telegram.org`.
   - If the host uses a proxy/VPN path for Telegram, test both routes explicitly: `curl --noproxy '*' https://api.telegram.org` versus the normal proxied curl. Also inspect process/env proxy settings (`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY`) for Hermes/OpenClaw PIDs. A direct Telegram timeout plus proxied success means the likely fault domain is the proxy/VPN egress path, not the bot process.

3. Inspect logs for the incident window:
   - Hermes: `~/.hermes/logs/gateway.log`, `~/.hermes/logs/errors.log`
   - OpenClaw: `~/.openclaw/logs/gateway.log`, `~/.openclaw/logs/gateway.err.log`
   - Look for: `Telegram network error`, `502 Bad Gateway`, `Timed out`, `polling resumed`, `fetch timeout`, `getMe`, `stale-socket`, `auto-restart`, `isolated polling ingress started`, `session_search`, `compression`, `unhealthy`.

4. Check routing separately from transport:
   - Compare topic source of truth (`/Users/xbr/.agentic-stack/chats.yaml`, `/Users/xbr/.openclaw/workspace/chats.md`) with the live runtime config.
   - A topic may be documented as default-responder but not present in live `free_response_topics`; with `require_mention: true`, the bot can look silent unless explicitly mentioned.

## Classification guide

- **Transport/ingress degraded:** process alive, Telegram API/polling errors in logs, later `polling resumed` or health-monitor restart.
- **Proxy/VPN egress degraded:** direct `api.telegram.org` may be blocked/unreachable from the host while the normal proxy works, or both Hermes and Bud show proxy/timeout errors at the same time. Treat shared proxy/Tailscale/egress as a common SPOF for both agents; smoke the proxy TCP path and Telegram through that path before restarting bots.
- **Routing/config issue:** process and polling healthy, inbound logged, but the topic lacks free-response/default routing or explicit mention handling.
- **Model/tooling slow:** inbound logged and agent started, but auxiliary/model/tool timeout warnings delay final response.
- **Process down:** launchd/systemd/Docker status missing, PID absent, health endpoint unavailable, recent crash/exit logs.

## Safe action pattern

- Do not blind-restart first. Capture logs and status, then decide.
- If logs show transient Telegram outage and polling already resumed, avoid restart; run smoke probes only.
- Restart only the smallest owner when current evidence shows stale polling did not recover: Telegram ingress/channel if available, then gateway as fallback.
- After any restart, verify: status command healthy, health endpoint live, Telegram inbound logs appear, outbound `Sending response`/message action succeeds.

## User-facing report style

For Mikhail, report in Russian, short and manager-style:

- Result first: `жив / degraded / down`.
- Root cause class in one line.
- Evidence bullets with MSK/PDT only if timing matters.
- Safe action taken/not taken.
- Next concrete fix/check.

Avoid long forensic dumps and avoid repeating a wrong interpretation after user correction; explicitly restate the corrected timeline before explaining.