---
name: live-meeting-notetaking
description: Attend or monitor live web meetings (Zoom/Meet/browser-based calls) for transcription, rolling notes, status updates, and final summaries. Covers browser and native app join, consent/permission expectations, audio/caption capture verification, and concise deliverable formats.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [meetings, transcription, Zoom, notes, productivity, audio, captions]
    related_skills: [macos-computer-use, teams-meeting-pipeline, zoom-meeting-capture, ocr-and-documents]
---

# Live Meeting Notetaking

Use this skill when the user asks the agent to join, monitor, transcribe, or summarize a live meeting/call/webinar (Zoom, Google Meet, browser-based conferencing, or similar), especially when they want rolling updates and a final summary.

For Microsoft Teams meetings that should go through the dedicated Graph transcript pipeline, prefer `teams-meeting-pipeline` first. Use this skill for ad-hoc live attendance or non-Teams meetings.

## First response: collect only what is necessary

Ask for missing items only if they are not already provided:
- meeting URL
- start time/timezone or “now”
- display name to join with
- passcode/waiting-room info if applicable
- consent/permission expectations for recording/transcription
- desired output cadence: status only, rolling chunks, or final summary

If the user gives broad permission (e.g. “browser is fine” / “install if needed”), act immediately and do not over-explain.

## Core policy

1. **Get the minimum join details**: meeting URL, start time (or "now"), display name, password/waiting-room notes, and whether recording/transcription is permitted.
2. **Be transparent about consent**: remind the user that meeting participants should be okay with recording/transcription. Do not secretly record if the user says recording is not allowed.
3. **Default meeting presence**: join muted, camera off, display name exactly as requested.
4. **Prefer reliability over purity**:
   - Native app is usually more reliable for audio and captions.
   - Browser join is acceptable when the app is missing, installation needs sudo/admin, or the user does not care.

## Join workflow

1. Prefer the browser path first for ad-hoc Zoom/Meet unless a native client is already installed and ready.
2. Join with camera off and microphone muted/no microphone.
3. Do not click OS/browser permission prompts for microphone/camera unless the user explicitly asked to use them.
4. For Zoom web:
   - open the join URL;
   - choose "Join from browser" / "Присоединиться в браузере" if offered;
   - choose "continue without microphone and camera";
   - enter the requested display name;
   - if waiting for host, report the waiting status and monitor.
   - If browser join lands inside an iframe or sparse DOM, inspect/navigate to the iframe `src` directly.
5. If native client installation needs sudo/admin credentials, do not block; fall back to browser and mention the installation limitation only briefly.

## Preflight checklist

- Confirm transcription path exists before the meeting starts:
  - Audio capture/recording capability, or
  - Built-in platform captions/transcript, or
  - User/cloud/local recording to process later.
- Check required tools only when needed: `ffmpeg`, `whisper` / `whisper-cli`, platform app/browser availability.
- If installation requires sudo/admin and cannot proceed non-interactively, do not block: use browser join or ask the user to install/approve only if browser join is inadequate.

## Status and cadence

When the user asks for updates:
- send an immediate current state (“joined and waiting”, “meeting started”, “blocked by password”, etc.);
- schedule or run periodic monitoring (e.g. every 2-3 minutes while waiting) when supported;
- keep a live foreground/main-session check after the meeting starts; do not rely only on cron/status pings, because fresh scheduled runs may lose the joined meeting state and cannot capture audio/notes by themselves;
- after the meeting starts, send the first capability status within a few minutes: whether audio/captions/chat are observable and whether transcription is working;
- if audio/captions/recording are not actually verified within the first few minutes, explicitly say “transcription is not working yet / nothing is being recorded yet” instead of waiting silently;
- send rolling chunks during the meeting, then a final overall summary.

Recommended rolling chunk format:
- **Status:** listening/transcribing/captions/chat-only/problem
- **Key points so far:** 2-5 bullets
- **Decisions:** bullets or “none yet”
- **Action items:** owner → task → deadline, if known
- **Risks/questions:** bullets

Final summary format:
- **Outcome:** one short paragraph
- **Decisions**
- **Action items**
- **Deadlines**
- **Risks/open questions**
- **Notable context**

Keep updates concise, especially for Telegram.

## Captions vs recording explanation

If the user asks what these mean:
- **Captions / live transcript:** real-time subtitles or transcript generated inside the meeting app, usually enabled by host or meeting settings.
- **Recording:** meeting audio/video saved locally or to the conferencing provider’s cloud; often the most reliable source for a transcript after the meeting.

If the user does not know meeting settings, proceed anyway and attempt the best available channel: captions, chat, visible meeting text, audio capture, or post-meeting recording.

## Transcription sources, in reliability order

1. Provider-generated transcript/captions, if available.
2. Cloud/local recording supplied after the meeting.
3. Direct audio capture from the browser/native client, then offline transcription with Whisper or equivalent.
4. Chat/logs/screenshare text and visual observation only.

Always label uncertainty. Do not imply a complete transcript if only partial sources were available.

## Pitfalls

- Do not promise reliable transcription before verifying an audio or caption source.
- Do not let "joined successfully" mask "not recording." Track these as separate states: joined/waiting, in meeting, capture source verified, transcript/notes flowing.
- Do not spend the whole session installing Zoom if browser join works and the user said either path is fine.
- Browser-based meeting audio capture may require environment-specific setup; treat it as a capability to verify after joining, not an assumption.
- Browser meeting pages may be localized; match labels by meaning, not exact English text.
- If using a scheduled monitor/cron for start notifications, remember it runs in a fresh session and is suitable for status pings only; it cannot preserve the main browser meeting state or serve as the actual note-taking/transcription process unless explicitly designed to do so.
- Before reporting "meeting started," verify real in-meeting UI such as participant count, Leave button, meeting controls, or visible participant/video tiles. Do not infer start from a transient loading/pre-join page.
- If waiting-room/host-not-started status persists, avoid noisy repeated messages; send concise periodic status only at the cadence the user requested.
- If a meeting requires credentials, 2FA, host login, or a permission dialog outside the stated scope, stop and ask.
- Do not save meeting-specific URLs, passcodes, participant names, or transcript content into persistent memory or the skill body.
- Joining successfully is not the same as verified transcription. Separately verify audio/captions/recording before promising transcript quality.

## Capturing/transcribing sources

Priority order for reliable transcription:

1. Use official transcript/captions/recording if enabled by host/meeting settings.
2. Use native app or OS-level audio capture if available and permitted.
3. Use browser audio/captions if accessible.
4. If live capture is unreliable, ask for or process the meeting recording afterward.

Track joining and capture as separate states: **joined**, **in meeting**, **capture verified**, **transcript/notes flowing**. Send a status within the first few minutes after start; if capture is not verified, say so explicitly instead of staying silent.

Avoid claiming a complete transcript unless capture was actually verified. If only partial notes are available, label them as partial.

## Deliverable format

For Mikhail, keep the final output essence-first and concise:

- **Главное:** 3–7 bullets.
- **Решения:** bullets.
- **Задачи:** owner → action → deadline, if known.
- **Риски/блокеры:** bullets.
- **Транскрипт:** attach or paste only if requested or useful.

If the meeting was not captured fully, add a one-line caveat at the end rather than a long apology.

For other users, adapt the format to their preferences while maintaining the same structure of outcome, decisions, action items, and risks.

## Reference files

- `references/zoom-browser-notetaking.md` — concise runbook for ad-hoc Zoom web attendance, status monitoring, and rolling summaries.
- `references/zoom-browser-capture-verification.md` — lessons/runbook for separating "joined" from "actually recording/transcribing" in Zoom web sessions.
- `references/zoom-web-join.md` — session-specific Zoom browser join sequence, Russian labels, and installation pitfalls.
