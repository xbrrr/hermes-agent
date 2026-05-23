# macOS per-app browser routing via VPS proxy

Use this when the user wants one browser (usually Chrome) to use a VPS/Tailscale-side proxy without changing the Mac's system route or enabling a full-device Tailscale exit node.

## Decision rule

- **Whole Mac traffic via VPS:** use Tailscale exit node after explicit approval.
- **Only Chrome/browser via VPS:** use a dedicated Chrome launcher with `--proxy-server` and a separate profile.
- **Do not call this an exit node:** per-app Chrome routing is HTTP/HTTPS proxying, not a Tailscale exit-node route.

## Baseline checks

```sh
# Tailscale full-device route state
/opt/homebrew/bin/tailscale debug prefs | egrep -i 'ExitNodeID|ExitNodeIP|ExitNodeAllowLANAccess|RouteAll|WantRunning|LoggedOut'
route -n get default | egrep 'gateway|interface|ifscope'

# macOS system proxy state
scutil --proxy | sed -n '1,120p'

# Proxy reachability and visible IP
nc -vz -G 3 100.100.1.1 18080
curl -x http://100.100.1.1:18080 -fsS --max-time 8 https://ifconfig.me
curl --noproxy '*' -fsS --max-time 8 https://ifconfig.me
```

If `ExitNodeID`/`ExitNodeIP` are empty and `scutil --proxy` has `HTTPEnable=0`, `HTTPSEnable=0`, `SOCKSEnable=0`, then GUI apps are not using a Tailscale exit node or system proxy. Only processes launched with proxy env or explicit proxy flags use the VPS.

## Chrome one-off launch

```sh
open -na "Google Chrome" --args \
  --user-data-dir="$HOME/.chrome-vps-profile" \
  --proxy-server="http://100.100.1.1:18080" \
  --proxy-bypass-list="<-loopback>" \
  --host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE 100.100.1.1" \
  --disable-quic \
  --no-first-run \
  --new-window "https://ifconfig.me"
```

Notes:
- Separate `--user-data-dir` keeps this isolated from normal Chrome.
- `--disable-quic` avoids UDP/QUIC bypassing the HTTP proxy path.
- `--host-resolver-rules` is a hardening guard against accidental direct DNS resolution; keep the proxy host excluded.

## Clickable app launcher

Create `~/Applications/Chrome via VPS.app`:

```sh
mkdir -p "$HOME/Applications/Chrome via VPS.app/Contents/MacOS"
cat > "$HOME/Applications/Chrome via VPS.app/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>Chrome via VPS</string>
  <key>CFBundleDisplayName</key><string>Chrome via VPS</string>
  <key>CFBundleIdentifier</key><string>com.xbr.chrome-via-vps</string>
  <key>CFBundleVersion</key><string>1.0</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>ChromeViaVPS</string>
  <key>LSMinimumSystemVersion</key><string>10.13</string>
  <key>LSUIElement</key><true/>
</dict>
</plist>
PLIST

cat > "$HOME/Applications/Chrome via VPS.app/Contents/MacOS/ChromeViaVPS" <<'SH'
#!/bin/zsh
set -euo pipefail
CHROME_APP="/Applications/Google Chrome.app"
PROFILE_DIR="$HOME/.chrome-vps-profile"
PROXY_URL="http://100.100.1.1:18080"
if [[ ! -d "$CHROME_APP" ]]; then
  /usr/bin/osascript -e 'display alert "Chrome via VPS" message "Google Chrome не найден в /Applications." as critical' >/dev/null 2>&1 || true
  exit 1
fi
mkdir -p "$PROFILE_DIR"
exec /usr/bin/open -na "$CHROME_APP" --args \
  --user-data-dir="$PROFILE_DIR" \
  --proxy-server="$PROXY_URL" \
  --proxy-bypass-list="<-loopback>" \
  --host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE 100.100.1.1" \
  --disable-quic \
  --no-first-run \
  --new-window "https://ifconfig.me"
SH

chmod +x "$HOME/Applications/Chrome via VPS.app/Contents/MacOS/ChromeViaVPS"
plutil -lint "$HOME/Applications/Chrome via VPS.app/Contents/Info.plist"
ln -sfn "$HOME/Applications/Chrome via VPS.app" "$HOME/Desktop/Chrome via VPS.app"
```

## Verification

```sh
open "$HOME/Applications/Chrome via VPS.app"
sleep 3
ps axww -o pid=,command= \
  | grep -F 'Google Chrome' \
  | grep -F '.chrome-vps-profile' \
  | grep -F '100.100.1.1:18080' \
  | grep -v grep
```

The launched window should show the VPS public IP on `https://ifconfig.me`.

## User-facing summary

Say clearly:
- “This affects only the special Chrome launcher/profile.”
- “Normal Chrome and other apps keep using the normal route unless system proxy or Tailscale exit node is enabled.”
- “This is not a full VPN; it is browser HTTP/HTTPS proxying through the VPS.”
