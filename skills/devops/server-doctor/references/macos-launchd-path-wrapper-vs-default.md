# macOS LaunchAgent PATH: wrapper env vs launchd default environment

## Problem

When a macOS LaunchAgent uses an env-wrapper script that sources a `.env` file to set `PATH`, the wrapper sees the correct PATH at exec time, but `launchctl print` reports only the `default environment = { PATH => /usr/bin:/bin:/usr/sbin:/sbin }`.

This discrepancy means:
- The main process launched by the wrapper inherits the correct PATH.
- Any subprocess spawned by the service that does NOT inherit the parent env (e.g., hooks, scheduled tasks, or tools that reset env) will fall back to the launchd default PATH and miss Homebrew binaries.

## Evidence pattern

```
launchctl print gui/$(id -u)/ai.openclaw.gateway | grep -A5 'environment ='
# Shows:
#   default environment = {
#     PATH => /usr/bin:/bin:/usr/sbin:/sbin
#   }

cat ~/.openclaw/service-env/ai.openclaw.gateway.env
# Shows:
#   export PATH='/opt/homebrew/opt/node@22/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
```

`openclaw gateway status` or `openclaw doctor` may report:
> Gateway service PATH missing required dirs: /opt/homebrew/bin, /opt/homebrew/sbin

## Root cause

launchd loads the `default environment` before the wrapper script runs. The wrapper's env changes apply only to the exec'd process tree, not to launchd's stored service environment.

## Fix options

### Option A: Declare PATH in plist EnvironmentVariables (recommended)

Add to the LaunchAgent plist:

```xml
<key>EnvironmentVariables</key>
<dict>
  <key>PATH</key>
  <string>/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
</dict>
```

Then reload:

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

Verify:

```bash
launchctl print gui/$(id -u)/ai.openclaw.gateway | grep PATH
```

### Option B: Use OpenClaw doctor --repair

If the service is managed by OpenClaw CLI:

```bash
openclaw doctor --repair
```

This will offer to patch the plist and reload the service. Requires drain/approval for live services.

## When to fix

- **Not urgent** if the main runtime works and no maintenance scripts are failing.
- **Urgent** if hooks, cron-like tasks, or non-interactive tooling within the service are failing with "command not found" for Homebrew packages.

## Verification

After fix:

```bash
launchctl print gui/$(id -u)/<service-label> | grep PATH
openclaw gateway status  # or equivalent status command
# Should report no PATH warnings
```

## Related

- `references/mac-mini-remote-access.md` — distinguishes Tailscale exit-node routing from macOS system proxy and per-process `HTTP_PROXY`.
- `references/agent-runtime-vps-proxy-vs-exit-node.md` — process-env, Cloudflare trace, launchd persistence checks.
