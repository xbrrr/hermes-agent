---
name: zoom-meeting-capture
description: Use when joining Zoom/online meetings for a user and producing recording, transcript, rolling notes, and final summary. Enforces preflight audio capture before meeting start and fail-fast status if audio/captions are unavailable.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [zoom, meetings, transcription, macos, audio-capture, whisper]
    related_skills: [macos-computer-use, ocr-and-documents]
---

# Zoom Meeting Capture

## Overview

This skill exists because simply joining Zoom is not enough. The job is only green when audio/text capture is verified before the meeting starts. Browser Zoom may let the agent observe the UI, but it does not guarantee an audio stream that Hermes can record. Treat audio capture as a separate dependency with an explicit preflight gate.

Primary local stack on Mikhail's Mac:

- `ffmpeg` for capture/chunking
- `whisper` wrapper / `whisper-cli` for transcription
- AudioTee system-audio capture when permissions work, no sudo required
- BlackHole/Loopback virtual audio fallback when system-audio capture is unavailable
- Zoom app preferred; browser Zoom acceptable only after audio preflight passes
- AudioTee capture is app-agnostic: it records whatever meeting audio is playing through macOS system output, so the same pipeline can capture Zoom, Yandex Telemost, Google Meet, Teams, Discord, browser calls, etc.; avoid overlapping audio sources because they mix into one transcript

## When to Use

Use this skill when the user asks you to:

- join a Zoom meeting instead of them
- listen and summarize a meeting
- transcribe a meeting live or after the fact
- prepare meeting-recorder infrastructure
- avoid silent failure in meeting capture

Do not rely on this skill for covert recording. Make sure the user has consent/authority and obey meeting recording policies.

## Hard Rule: Preflight or Fail

Before saying “I can record/transcribe this meeting”, run a real audio preflight.

Preferred command:

```bash
~/.hermes/scripts/zoom_meeting_recorder.py doctor
~/.hermes/scripts/zoom_meeting_recorder.py preflight-system --seconds 15 --transcribe
```

Classic BlackHole fallback:

```bash
~/.hermes/scripts/zoom_meeting_recorder.py preflight --device "BlackHole 2ch" --seconds 15 --transcribe
```

Green means:

- an actual WAV file is created
- file has non-trivial size
- Whisper produces a transcript or at least proves decode path works
- you can tell the user: `preflight green: audio capture + Whisper are working`

Red means:

- do not promise transcription
- tell the user immediately what is missing
- ask for Zoom recording/captions or permission/admin setup

## Local Helper Script

Helper path:

```bash
/Users/xbr/.hermes/scripts/zoom_meeting_recorder.py
```

Commands:

```bash
# Diagnose stack and show missing prerequisites
~/.hermes/scripts/zoom_meeting_recorder.py doctor

# No-BlackHole system-audio preflight via AudioTee
~/.hermes/scripts/zoom_meeting_recorder.py preflight-system --seconds 15 --transcribe

# Chunked system-audio recording, 5-min chunks
~/.hermes/scripts/zoom_meeting_recorder.py record-system --chunk-seconds 300

# BlackHole/Loopback preflight
~/.hermes/scripts/zoom_meeting_recorder.py preflight --device "BlackHole 2ch" --seconds 15 --transcribe

# BlackHole/Loopback chunked recording
~/.hermes/scripts/zoom_meeting_recorder.py record --device "BlackHole 2ch" --chunk-seconds 300

# Transcribe a folder of chunks after/while recording
~/.hermes/scripts/zoom_meeting_recorder.py transcribe ~/Recordings/meetings/<session_dir> --language auto
```

Important current-state note: AudioTee builds successfully, and current preflight with `--tone --transcribe` is green on Mikhail's Mac. If macOS Settings does not show a “System Audio Recording” entry, do not keep asking the user to find it; rerun `preflight-system --tone --transcribe`. If that passes, permission/capture is already usable. If it fails, use browser/Zoom captions or BlackHole/Zoom.app fallback.

## One-Time Setup

No-sudo path, preferred on macOS 14.2+:

```bash
mkdir -p ~/.hermes/tools
cd ~/.hermes/tools
git clone https://github.com/makeusabrew/audiotee.git audiotee
cd audiotee
swift build -c release
```

Classic virtual-device fallback, requires admin password and reboot:

```bash
/opt/homebrew/bin/brew install --cask zoom blackhole-2ch
/opt/homebrew/bin/brew install ffmpeg whisper-cpp switchaudio-osx sox
```

After BlackHole install:

1. Reboot if installer asks.
2. Open Audio MIDI Setup.
3. Create Multi-Output Device = current speakers/headphones + BlackHole 2ch.
4. In Zoom Settings → Audio → Speaker, select the Multi-Output Device.
5. Keep mic muted unless the user explicitly wants the bot to speak.
6. Grant Microphone permission to terminal/Hermes/ffmpeg when prompted.
7. Run the BlackHole preflight command above.

## Meeting Runbook

### 10–15 minutes before meeting

1. Load this skill.
2. Run `doctor`.
3. Run preflight with the path you intend to use.
4. If preflight red, do not continue silently. Tell the user the exact missing piece.
5. Join Zoom as the requested name, camera off, mic muted.
6. Start chunked recorder only after preflight green.

### During meeting

Record in small chunks:

```bash
~/.hermes/scripts/zoom_meeting_recorder.py record-system --chunk-seconds 300
```

Every 5–10 minutes:

1. Transcribe completed chunks.
2. Send compact rolling update:
   - key points
   - decisions
   - action items
   - risks/blockers
   - confidence level

If no audio/text after 2–3 minutes from start, tell the user immediately. Do not wait 15 minutes.

### After meeting

1. Stop recorder.
2. Transcribe all chunks.
3. Merge transcript.
4. Send final summary:
   - TL;DR
   - decisions
   - tasks/owners/deadlines
   - unresolved questions
   - links/files/screenshares observed
   - transcript path or media path if useful

## Better Existing Wheels / Research Findings

Do not reinvent everything if one of these fits:

- **Meetily** — open-source local/privacy-first meeting assistant, macOS/Windows, Rust, Whisper/Parakeet/local notes. Good candidate for local product-like recorder. https://github.com/Zackriya-Solutions/meetily
- **Vexa** — open-source meeting bot/transcription API for Google Meet, Teams, Zoom; self-hosted; real-time WebSocket transcripts; MCP server. Good candidate for server/bot path. https://github.com/Vexa-ai/vexa
- **Attendee** — open-source meeting bot API for Zoom/Google Meet; Django/Docker; reduces cost vs closed vendors. https://github.com/attendee-labs/attendee
- **screenappai/meeting-bot** — Playwright/TypeScript bot that joins and records Zoom/Meet/Teams. Useful reference for browser automation. https://github.com/screenappai/meeting-bot
- **Zoom Arlo / RTMS starter pattern** — official Zoom RTMS reference for live transcripts without a bot; requires Zoom app/platform setup. https://github.com/zoom/arlo and https://github.com/zoom/rtms-meeting-assistant-starter-kit
- **Recall.ai** — hosted meeting bot API; quickest reliable cross-platform production path if paid SaaS is acceptable. https://www.recall.ai
- **AudioTee** — CLI system-output capture via Core Audio taps, no BlackHole; requires macOS 14.2+ and System Audio Recording permission. https://github.com/makeusabrew/audiotee
- **BlackHole** — classic virtual audio driver for macOS. https://github.com/ExistentialAudio/BlackHole

Decision heuristic:

- arbitrary external Zoom link from Mikhail: use browser Zoom or Zoom.app to join as muted/camera-off participant, capture local system audio via AudioTee, chunk WAV, transcribe with Whisper, summarize; do not depend on Zoom RTMS/Marketplace credentials
- personal/local/private and one Mac: AudioTee first; BlackHole fallback; Meetily if product-like app desired
- one meeting at a time on one Mac: local AudioTee system-audio capture is acceptable
- multiple simultaneous meetings: do not run them on one shared macOS output, because audio sources mix into one transcript; use one isolated worker per meeting (separate Mac/VM/cloud browser/container with its own audio sink) or a meeting-bot platform/API
- reliable bot that joins external meetings at scale: Vexa/Attendee/Recall.ai
- Zoom-admin-controlled org: RTMS/Arlo/Zoom App
- post-meeting only: Zoom cloud recording + Zoom API + Whisper/ASR

## Meetily + Arlo Local Install Notes

Current install paths on Mikhail's Mac:

```bash
~/Applications/Meetily.app
~/.hermes/tools/zoom-rtms/arlo
~/.hermes/tools/zoom-rtms/rtms-meeting-assistant-starter-kit
~/.hermes/scripts/arlo-rtms.sh
```

Arlo verified local stack uses Homebrew `colima`, `docker`, `docker-compose`, `docker-buildx`, and `ngrok`. Docker Desktop cask can fail in headless Hermes because it needs sudo for `/usr/local/cli-plugins`; prefer Colima.

Apple Silicon Arlo quirk: `rtms` is declared `linux/amd64`. Build it explicitly with buildx before `docker compose up`:

```bash
cd ~/.hermes/tools/zoom-rtms/arlo
docker buildx build --platform linux/amd64 --load -t arlo-rtms:latest ./rtms
docker compose up -d
npm test
```

Convenience commands:

```bash
~/.hermes/scripts/arlo-rtms.sh start
~/.hermes/scripts/arlo-rtms.sh status
~/.hermes/scripts/arlo-rtms.sh test
~/.hermes/scripts/arlo-rtms.sh logs backend
~/.hermes/scripts/arlo-rtms.sh stop
```

Before real Zoom RTMS use, replace dev dummy values in `~/.hermes/tools/zoom-rtms/arlo/.env` with real Zoom Marketplace `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`, `ZOOM_WEBHOOK_TOKEN`, and set `PUBLIC_URL` to an ngrok/static HTTPS domain. RTMS access must be enabled/approved by Zoom.

## Common Pitfalls

1. **Joining without recording.** Joining Zoom is not progress unless audio/captions are captured.
2. **Trusting browser Zoom.** Browser UI access does not imply a recordable audio stream.
3. **No preflight.** Always record and transcribe a 10–15 second sample before the meeting.
4. **Silent failure.** If no transcript in 2–3 minutes after start, notify the user immediately.
5. **Meeting UI/session drop.** Browser meeting sessions can silently navigate to `about:blank`, return to the lobby, or drop from the participant list while the audio recorder continues. During live capture, monitor meeting presence every few minutes; if dropped, rejoin immediately and report possible gap in coverage.
6. **No permissions.** macOS may block System Audio Recording, Microphone, or Screen Recording. A tool can build successfully and still capture zero frames.
6. **No chunking.** Long recordings are harder to salvage; use 5-minute chunks.
7. **No fallback.** Ask for Zoom recording/captions if local audio is red.
8. **No consent.** Confirm recording/transcription is allowed.

## Delivery Pitfalls

- When sending final artifacts (PDF, transcript, audio chunks), verify the user actually received the attachment, not just that the file exists locally. If Hermes/Gateway media delivery warns or fails for a PDF/document, use the Telegram Bot API `sendDocument` fallback and require `ok: true` before claiming delivery. See `references/telegram-pdf-delivery.md`.

## Verification Checklist

- [ ] `doctor` run and output reviewed
- [ ] preflight recorded actual audio
- [ ] Whisper transcript path exists
- [ ] Zoom joined as requested name
- [ ] mic muted / camera off unless requested otherwise
- [ ] recorder running in chunks
- [ ] first status sent within 2–3 minutes of meeting start
- [ ] rolling updates sent
- [ ] final summary sent
- [ ] final artifacts/attachments verified as delivered (or resent via documented fallback)
