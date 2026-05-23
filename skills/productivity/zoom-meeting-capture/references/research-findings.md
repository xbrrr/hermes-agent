# Research Findings: Zoom/Meeting Capture

Source path used: Perplexity Sonar helper with `search_sources=["social","web"]`, plus GitHub API search. Avoided direct x.com scraping.

## Strong candidates

- Meetily — local/privacy-first meeting assistant, macOS/Windows, Rust, Whisper/Parakeet/local notes. https://github.com/Zackriya-Solutions/meetily
- Vexa — open-source meeting bot/transcription API for Google Meet, Teams, Zoom; self-hosted; real-time WebSocket transcripts; MCP server. https://github.com/Vexa-ai/vexa
- Attendee — open-source meeting bot API for Zoom/Google Meet; Django/Docker; reduces cost vs closed vendors. https://github.com/attendee-labs/attendee
- screenappai/meeting-bot — Playwright/TypeScript bot for joining/recording Zoom/Meet/Teams. https://github.com/screenappai/meeting-bot
- Zoom Arlo — official RTMS reference for live transcripts without a bot. https://github.com/zoom/arlo
- Zoom RTMS starter kit — official meeting assistant starter pattern. https://github.com/zoom/rtms-meeting-assistant-starter-kit
- AudioTee — Core Audio tap CLI for system output capture, no BlackHole. https://github.com/makeusabrew/audiotee
- BlackHole — classic macOS virtual audio driver. https://github.com/ExistentialAudio/BlackHole
- Recall.ai — hosted meeting bot API. https://www.recall.ai

## Key conclusions

1. Zoom desktop client is not a reliable programmable automation surface; use SDK/RTMS/bot service or local capture.
2. Browser Zoom is acceptable for joining/observing but should not be trusted for audio capture without a separate preflight.
3. macOS has no simple built-in `Stereo Mix`; capture needs AudioTee/CoreAudio taps, ScreenCaptureKit, BlackHole/Loopback, Zoom recording, or a bot API.
4. For this Mac, fastest no-sudo path is AudioTee -> ffmpeg -> Whisper, but macOS System Audio Recording permission must be green.
5. For production-grade external meeting attendance, prefer Vexa/Attendee/Recall.ai rather than DIY browser capture.
6. For local private assistant UX, investigate Meetily before building a full app from scratch.
