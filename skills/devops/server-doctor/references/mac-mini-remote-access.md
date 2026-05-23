# Mac mini remote access repair pattern

Session distilled pattern for a macOS host where AnyDesk repeatedly stopped accepting connections.

## Chosen architecture

- Primary: Tailscale mesh VPN + SSH/VNC.
- Fallback: AnyDesk.
- Do not treat AnyDesk as the main channel if it has a history of instability.

## Baseline probes used

```sh
hostname
sw_vers
date
id
who
ifconfig
curl -fsS --max-time 5 https://ifconfig.me || true

# Tailscale
/opt/homebrew/bin/tailscale status --self
/opt/homebrew/bin/tailscale ip -4
/opt/homebrew/bin/tailscale debug prefs | egrep -i 'RunSSH|WantRunning|LoggedOut|ShieldsUp|CorpDNS|RouteAll'

# Remote ports through Tailscale IP
for p in 22 5900 7070; do nc -vz -G 3 <tailscale-ip> "$p"; done

# AnyDesk
/Applications/AnyDesk.app/Contents/MacOS/AnyDesk --get-status
/Applications/AnyDesk.app/Contents/MacOS/AnyDesk --get-id

# launchd and syntax
plutil -lint ~/Library/LaunchAgents/*.plist
zsh -n /path/to/watchdog.sh
launchctl print gui/$(id -u)/<label>
```

## macOS details that mattered

- Screen Sharing/VNC can be verified by connecting to port `5900` and receiving an RFB banner.
- `launchctl print system/com.openssh.sshd` may show `not running` even when socket activation is ready; a successful port 22 connection is better evidence of reachability.
- Tailscale SSH can be enabled with:

```sh
/opt/homebrew/bin/tailscale up --ssh --accept-dns=true --accept-routes=true
```

- User LaunchAgent logs should normally go under `~/Library/Logs/`, not `/var/log`, unless running as root.
- A plist that accidentally has shell commands appended after `</plist>` can still appear in a workflow but is invalid; always `plutil -lint` before loading.

## Example health-check shape

A useful health job should log:

- Tailscale status and IP.
- VPN-path reachability of SSH `22`.
- VPN-path reachability of VNC `5900`.
- Fallback remote app status/ID.
- Repair attempt only when unhealthy.

For macOS, package as a LaunchAgent with `RunAtLoad` and `StartInterval`, then verify with:

```sh
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/<label>.plist
launchctl kickstart -k gui/$(id -u)/<label>
launchctl print gui/$(id -u)/<label>
tail -30 ~/Library/Logs/<health>.log
```

## User-facing access instructions template

Mac:

- Install/login Tailscale in the same tailnet.
- GUI fast path: press `Cmd+K`, paste `vnc://<tailscale-ip>`, Connect.
- GUI menu path, if needed: click the desktop/Finder first, then top macOS menu bar → Go → Connect to Server → `vnc://<tailscale-ip>`.
- Shell: `ssh <user>@<tailscale-ip>`.

Windows:

- Install/login Tailscale in the same tailnet.
- GUI: RealVNC/TigerVNC/TightVNC → `<tailscale-ip>:5900`.
- Shell: PowerShell/Windows Terminal → `ssh <user>@<tailscale-ip>`.

Fallback:

- Use AnyDesk ID from baseline.

## Screen Sharing/VNC auth succeeds but macOS blocks viewing

A user-facing error like “Screen Sharing is not allowed on device `<ip>`; turn Screen Sharing or Remote Management off/on” can occur even when network checks are green.

Diagnostic pattern:

```sh
# Port/banner can be healthy while viewing is blocked
nc -vz -G 3 <tailscale-ip> 5900
python3 - <<'PY'
import socket, binascii
s=socket.create_connection(('<tailscale-ip>',5900),5)
s.settimeout(3)
proto=s.recv(12); print(proto); s.close()
PY

# Check the real failure in unified logs
log show --style compact --last 15m --predicate 'process == "screensharingd"' \
  | egrep -i 'Authentication: SUCCEEDED|Unable to capture screen|screen sharing is restricted|not allowed'
```

Important distinctions:

- `RFB ...` banner and open `5900` prove reachability, not permission to view.
- `Authentication: SUCCEEDED` followed by `Unable to capture screen` points to macOS Screen Sharing/Remote Management permission/state, not Tailscale.
- `launchctl kickstart -k system/com.apple.screensharing` is safe to try, but may not clear the permission block.
- Full repair normally requires root/admin on the host:

```sh
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart \
  -activate -configure -access -on -users <user> -privs -all -restart -agent
```

If the agent lacks passwordless sudo, say so directly and give SSH + sudo command; use AnyDesk as fallback if online.

## AnyDesk watchdog pitfalls

- AnyDesk process layouts vary by version: healthy states may include `--local-service`, `--control`, and/or the root `--service`. Watchdogs should trust `--get-status=online` plus expected ID and at least one live backend/control/service process, not require only `--local-service`.
- If syncing AnyDesk identity from `~/.anydesk` to `/etc/anydesk` as an admin user with group-writable files, avoid `cp -p` for the final user→`/etc` copy: preserving owner/mode/timestamps can emit `utimensat/chmod` permission errors even when content is writable. Use plain `cp` after backing up.

## Tailscale exit node vs proxy env on Mac mini

When diagnosing “VPN does not work” or “route all Mac mini traffic through the VPS,” distinguish three layers before changing routes:

1. **Tailscale exit node selection** — authoritative for full-device routing:

```sh
/opt/homebrew/bin/tailscale status --self
/opt/homebrew/bin/tailscale status | egrep -i 'offers exit node|<exit-node-name>|<exit-node-ip>'
/opt/homebrew/bin/tailscale debug prefs | egrep -i 'ExitNodeID|ExitNodeIP|ExitNodeAllowLANAccess|RouteAll|WantRunning|LoggedOut'
route -n get default | egrep 'gateway|interface|ifscope'
```

If `ExitNodeID`/`ExitNodeIP` are empty, no app is using a Tailscale exit node as a full-device route even if an exit-node host is available.

2. **macOS system proxy** — affects GUI/system clients that honor macOS network proxy settings:

```sh
scutil --proxy | sed -n '1,120p'
```

`HTTPEnable=0`, `HTTPSEnable=0`, and `SOCKSEnable=0` mean no system proxy is configured.

3. **Process environment proxy** — affects only processes launched with those env vars and only if the program honors them:

```sh
for v in http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY; do printf '%s=' "$v"; launchctl getenv "$v" || true; done
env | egrep -i '^(http|https|all)_proxy='
printf 'direct: '; curl --noproxy '*' -fsS --max-time 8 https://ifconfig.me; printf '\n'
printf 'env/proxy: '; curl -fsS --max-time 8 https://ifconfig.me; printf '\n'
```

If direct IP differs from env/proxy IP, only proxy-aware CLI/processes in that environment are using the VPS. Browser/GUI/system traffic is not necessarily routed through it.

### Enabling full-device routing through the exit node

For the known Mac mini setup, the safe full-device route is Tailscale exit node with LAN access preserved:

```sh
/opt/homebrew/bin/tailscale set --exit-node=100.100.1.1 --exit-node-allow-lan-access=true
```

Use this only after explicit approval because it changes routing for the whole Mac mini. Avoid Karing full-TUN as the unattended default when remote access matters; it has higher risk of breaking routes/SSH/VNC. Prefer Tailscale exit node first, then verify and keep rollback ready:

```sh
# verify
/opt/homebrew/bin/tailscale debug prefs | egrep -i 'ExitNodeID|ExitNodeIP|ExitNodeAllowLANAccess|RouteAll'
curl --noproxy '*' -fsS --max-time 8 https://ifconfig.me
nc -vz -G 3 100.82.112.95 22
nc -vz -G 3 100.82.112.95 5900

# rollback
/opt/homebrew/bin/tailscale set --exit-node=
```

User-facing wording: “Exit node is not per-app here. If `ExitNodeIP` is empty, no app is using Tailscale exit node; only processes with `HTTP_PROXY/HTTPS_PROXY` may be going via VPS.”

## Reporting style

Keep final report short:

- Architecture: primary/fallback.
- Current verified endpoints.
- What was fixed.
- Exact user connection steps.
- Residual risks: powered off, no internet, Tailscale/permissions/session failure.
