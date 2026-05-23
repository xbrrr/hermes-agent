# Agent runtime traffic: VPS proxy vs Tailscale exit node

Use this when debugging why Hermes/Bud/OpenClaw can reach region-blocked providers even though the Mac/host has no full-device exit node enabled.

## Key distinction

- **Tailscale exit node** is OS/device-level routing. If disabled, clean processes on the Mac can still exit directly from the ISP/public IP.
- **HTTP/HTTPS proxy env** is process-level routing. A gateway or worker can reach ChatGPT/Anthropic/OpenAI through a VPS proxy even when the host exit node is off, if that process has `HTTP_PROXY`/`HTTPS_PROXY`/lowercase variants.
- **macOS system proxy** is separate from both. `scutil --proxy` can show no system proxy while agent processes still use env proxy.

## Evidence recipe

1. Check host clean/direct IP and proxied IP separately:

```bash
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy -u ALL_PROXY -u all_proxy curl -4 -s https://ifconfig.me
curl -4 -s https://ifconfig.me
```

2. Check provider-side geography, not only `ifconfig`:

```bash
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy curl -s https://chatgpt.com/cdn-cgi/trace | egrep 'ip=|colo=|loc='
curl -s https://chatgpt.com/cdn-cgi/trace | egrep 'ip=|colo=|loc='
```

3. Check the live process env, not just the current shell:

```bash
python3 - <<'PY'
import re, subprocess
for pid, name in [('PID_HERE', 'service')]:
    out = subprocess.run(['ps', 'eww', '-p', pid], capture_output=True, text=True).stdout
    print(f'== {name} pid {pid} proxy env ==')
    for k in ['HTTP_PROXY','HTTPS_PROXY','http_proxy','https_proxy','ALL_PROXY','all_proxy','NO_PROXY','no_proxy']:
        m = re.search(r'(?:^|\\s)' + re.escape(k) + r'=([^\\s]+)', out)
        print(f'{k}={m.group(1) if m else ""}')
PY
```

4. Check launch persistence separately:

```bash
plutil -p ~/Library/LaunchAgents/<label>.plist | egrep -i 'EnvironmentVariables|HTTP_PROXY|HTTPS_PROXY|NO_PROXY|Program|Label'
launchctl print gui/$(id -u)/<label> | egrep -i 'environment|HTTP_PROXY|HTTPS_PROXY|NO_PROXY|pid|program ='
```

## Interpretation pattern

- If current shell has proxy but launchd plist does not, the current session may work accidentally while the next restart loses proxy routing.
- If OpenClaw/Bud has proxy env and Hermes gateway does not, Bud may reach blocked providers while Hermes/Telegram does not after restart.
- If ChatGPT Codex works from Hermes despite the launchd plist lacking proxy env, verify whether the live request path inherited a shell snapshot or credential helper that has proxy; do not call it durable until the LaunchAgent/unit explicitly declares proxy env and a restart smoke confirms it.

## Persistent fix pattern

For macOS launchd agents, add both uppercase and lowercase proxy variables plus `NO_PROXY` to the service plist `EnvironmentVariables`, then drain/restart/smoke:

- `HTTP_PROXY=http://<tailnet-vps-ip>:<port>`
- `HTTPS_PROXY=http://<tailnet-vps-ip>:<port>`
- `http_proxy=http://<tailnet-vps-ip>:<port>`
- `https_proxy=http://<tailnet-vps-ip>:<port>`
- `NO_PROXY=localhost,127.0.0.1,::1,<vps-tailnet-ip>,<host-tailnet-ip>`
- `no_proxy=...same...`

Do not enable full-device exit-node routing unless the user explicitly wants all host traffic routed through the VPS and accepts the rollback plan.