#!/usr/bin/env python3
"""Local macOS Zoom/meeting recorder helper for Hermes.

Primary path: Zoom app/browser -> BlackHole 2ch virtual device -> ffmpeg chunked WAV -> whisper.
This script is intentionally conservative: it never joins Zoom or clicks UI; it verifies/records/transcribes.
"""
from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

HOME = Path.home()
BREW = Path("/opt/homebrew/bin/brew")
FFMPEG = Path("/opt/homebrew/bin/ffmpeg")
SWITCH = Path("/opt/homebrew/bin/SwitchAudioSource")
WHISPER = Path("/Users/xbr/.local/bin/whisper")
AUDIOTEE = HOME / ".hermes/tools/audiotee/.build/release/audiotee"
DEFAULT_MODEL = HOME / ".local/share/whisper/ggml-base.bin"
DEFAULT_ROOT = HOME / "Recordings/meetings"
DEFAULT_DEVICE = "BlackHole 2ch"


def run(cmd: list[str], check: bool = False, capture: bool = True, timeout: int | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
        timeout=timeout,
    )


def have(path_or_cmd: str | Path) -> bool:
    p = Path(path_or_cmd)
    return p.exists() if p.is_absolute() else shutil.which(str(path_or_cmd)) is not None


def ffmpeg_devices() -> str:
    if not have(FFMPEG):
        return ""
    proc = run([str(FFMPEG), "-hide_banner", "-f", "avfoundation", "-list_devices", "true", "-i", ""], timeout=20)
    return proc.stdout or ""


def parse_audio_devices(text: str) -> list[str]:
    devices: list[str] = []
    in_audio = False
    for line in text.splitlines():
        if "AVFoundation audio devices:" in line:
            in_audio = True
            continue
        if in_audio:
            m = re.search(r"\]\s*\[(\d+)\]\s*(.+)$", line)
            if m:
                devices.append(m.group(2).strip())
    return devices


def switch_devices(kind: str = "output") -> list[str]:
    if not have(SWITCH):
        return []
    args = [str(SWITCH), "-a"] + (["-t", kind] if kind else [])
    proc = run(args, timeout=10)
    return [x.strip() for x in (proc.stdout or "").splitlines() if x.strip()]


def doctor(args: argparse.Namespace) -> int:
    print("## Zoom meeting recorder doctor")
    checks = {
        "ffmpeg": have(FFMPEG),
        "whisper wrapper": have(WHISPER),
        "whisper model": DEFAULT_MODEL.exists(),
        "SwitchAudioSource": have(SWITCH),
        "AudioTee system-audio capture": have(AUDIOTEE),
        "Zoom.app": Path("/Applications/zoom.us.app").exists(),
        "BlackHole output device": any("BlackHole" in d for d in switch_devices("output")),
    }
    for k, ok in checks.items():
        print(f"{k}: {'OK' if ok else 'MISSING'}")

    raw = ffmpeg_devices()
    audio = parse_audio_devices(raw)
    print("\nAVFoundation audio inputs visible to ffmpeg:")
    if audio:
        for d in audio:
            print(f"- {d}")
    else:
        print("- NONE")
        print("  Likely causes: no virtual audio device installed, or Terminal/ffmpeg lacks Microphone permission.")

    print("\nRecommended setup paths:")
    print("  A) No-sudo preferred on macOS 14.2+: AudioTee -> ffmpeg -> whisper (already built if AudioTee=OK).")
    print("     Preflight: ~/.hermes/scripts/zoom_meeting_recorder.py preflight-system --seconds 15 --transcribe")
    print("  B) Classic virtual-device fallback (requires admin password + reboot for BlackHole):")
    print("     /opt/homebrew/bin/brew install --cask zoom blackhole-2ch")
    print("     /opt/homebrew/bin/brew install switchaudio-osx sox ffmpeg whisper-cpp")
    print("     Audio MIDI Setup -> Multi-Output Device = Speakers/Headphones + BlackHole 2ch")
    print("     Zoom Settings -> Audio -> Speaker = that Multi-Output device; Microphone stays muted/normal.")
    print("Grant System Audio Recording/Microphone permission to the terminal/Hermes process when prompted.")

    if args.test:
        return preflight(args)
    return 0 if all(checks.values()) and audio else 1


def preflight(args: argparse.Namespace) -> int:
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    wav = out_dir / f"preflight_{time.strftime('%Y%m%d_%H%M%S')}.wav"
    device = args.device
    print(f"\nRecording {args.seconds}s preflight from audio device: {device!r}")
    cmd = [
        str(FFMPEG), "-hide_banner", "-y",
        "-f", "avfoundation", "-i", f":{device}",
        "-t", str(args.seconds),
        "-ac", "1", "-ar", "16000", "-sample_fmt", "s16",
        str(wav),
    ]
    print("$", " ".join(shlex.quote(x) for x in cmd))
    proc = run(cmd, timeout=args.seconds + 30)
    if proc.returncode != 0 or not wav.exists() or wav.stat().st_size < 8000:
        print(proc.stdout or "")
        print("PRELIGHT_FAIL: no usable audio file. Fix BlackHole/audio permissions before relying on this for a meeting.")
        return 2
    print(f"PRELIGHT_AUDIO_OK: {wav} ({wav.stat().st_size} bytes)")
    if args.transcribe:
        return transcribe_file(wav, out_dir)
    return 0


def record(args: argparse.Namespace) -> int:
    out_dir = Path(args.out_dir).expanduser() / time.strftime("%Y%m%d_%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern = str(out_dir / "chunk_%Y%m%d_%H%M%S.wav")
    cmd = [
        str(FFMPEG), "-hide_banner", "-y",
        "-f", "avfoundation", "-i", f":{args.device}",
        "-ac", "1", "-ar", "16000", "-sample_fmt", "s16",
        "-f", "segment", "-segment_time", str(args.chunk_seconds), "-strftime", "1",
        pattern,
    ]
    if args.duration:
        cmd[5:5] = ["-t", str(args.duration)]
    print(f"Recording chunks to: {out_dir}")
    print("$", " ".join(shlex.quote(x) for x in cmd))
    proc = subprocess.Popen(cmd, text=True)
    try:
        return proc.wait()
    except KeyboardInterrupt:
        print("Stopping recorder...")
        proc.send_signal(signal.SIGINT)
        try:
            return proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            return proc.wait()


def _audiotee_ffmpeg_wav(out: Path, seconds: int | None = None, segment_seconds: int | None = None) -> int:
    """Capture system output via AudioTee and encode to WAV with ffmpeg.

    AudioTee emits mono s16le when --sample-rate is provided.
    """
    if not have(AUDIOTEE):
        print(f"AUDIOTEE_MISSING: {AUDIOTEE}")
        return 127
    out.parent.mkdir(parents=True, exist_ok=True)
    tee_cmd = [str(AUDIOTEE), "--sample-rate", "16000"]
    ff_cmd = [
        str(FFMPEG), "-hide_banner", "-y",
        "-f", "s16le", "-ar", "16000", "-ac", "1", "-i", "pipe:0",
        "-ac", "1", "-ar", "16000", "-sample_fmt", "s16",
    ]
    if seconds:
        ff_cmd += ["-t", str(seconds), str(out)]
    else:
        assert segment_seconds is not None
        ff_cmd += ["-f", "segment", "-segment_time", str(segment_seconds), "-strftime", "1", str(out)]

    print("$", " ".join(shlex.quote(x) for x in tee_cmd), "|", " ".join(shlex.quote(x) for x in ff_cmd))
    tee = subprocess.Popen(tee_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ff = subprocess.Popen(ff_cmd, stdin=tee.stdout, text=False)
    if tee.stdout:
        tee.stdout.close()
    try:
        rc = ff.wait(timeout=(seconds + 30) if seconds else None)
    except subprocess.TimeoutExpired:
        print("FFMPEG_TIMEOUT: no audio frames arrived before timeout; stopping capture.")
        ff.terminate()
        try:
            rc = ff.wait(timeout=5)
        except subprocess.TimeoutExpired:
            ff.kill()
            rc = ff.wait()
    except KeyboardInterrupt:
        print("Stopping system recorder...")
        ff.send_signal(signal.SIGINT)
        rc = ff.wait(timeout=10)
    finally:
        if tee.poll() is None:
            tee.terminate()
            try:
                tee.wait(timeout=5)
            except subprocess.TimeoutExpired:
                tee.kill()
        err = tee.stderr.read().decode("utf-8", "replace") if tee.stderr else ""
        if err.strip():
            print("AudioTee stderr:")
            print(err.strip()[-2000:])
    return rc


def preflight_system(args: argparse.Namespace) -> int:
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    wav = out_dir / f"system_preflight_{time.strftime('%Y%m%d_%H%M%S')}.wav"
    tone_proc = None
    if args.tone:
        tone = out_dir / "_preflight_tone.wav"
        run([str(FFMPEG), "-hide_banner", "-y", "-f", "lavfi", "-i", f"sine=frequency=880:duration={args.seconds}", "-ac", "1", "-ar", "16000", str(tone)], timeout=20)
        # Start tone just after AudioTee starts listening. This is intentionally audible.
        tone_proc = subprocess.Popen(["/bin/bash", "-lc", f"sleep 1; afplay {shlex.quote(str(tone))}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Playing short audible test tone during preflight.")
    print(f"Recording {args.seconds}s SYSTEM AUDIO preflight via AudioTee")
    rc = _audiotee_ffmpeg_wav(wav, seconds=args.seconds)
    if tone_proc and tone_proc.poll() is None:
        tone_proc.terminate()
    if rc != 0 or not wav.exists() or wav.stat().st_size < 8000:
        print("PREFLIGHT_SYSTEM_FAIL: no usable system-audio file. Grant System Audio Recording permission or use BlackHole fallback.")
        return rc or 2
    print(f"PREFLIGHT_SYSTEM_AUDIO_OK: {wav} ({wav.stat().st_size} bytes)")
    if args.transcribe:
        return transcribe_file(wav, out_dir)
    return 0


def record_system(args: argparse.Namespace) -> int:
    out_dir = Path(args.out_dir).expanduser() / time.strftime("%Y%m%d_%H%M%S_system")
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern = out_dir / "chunk_%Y%m%d_%H%M%S.wav"
    print(f"Recording SYSTEM AUDIO chunks to: {out_dir}")
    return _audiotee_ffmpeg_wav(pattern, segment_seconds=args.chunk_seconds)


def transcribe_file(wav: Path, out_dir: Path, language: str = "auto") -> int:
    cmd = [str(WHISPER), str(wav), "--output_dir", str(out_dir), "--output_format", "txt", "--language", language]
    env = os.environ.copy()
    env.setdefault("WHISPER_CPP_MODEL", str(DEFAULT_MODEL))
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    if proc.stdout:
        print(proc.stdout)
    txt = out_dir / (wav.name + ".txt")
    if txt.exists():
        print(f"TRANSCRIPT_OK: {txt}")
        return 0
    print(f"TRANSCRIPT_FAIL for {wav}")
    return proc.returncode or 3


def transcribe(args: argparse.Namespace) -> int:
    in_dir = Path(args.path).expanduser()
    files = sorted(list(in_dir.glob("*.wav")) + list(in_dir.glob("*.mp3")) + list(in_dir.glob("*.m4a")))
    if not files:
        print(f"No audio files found in {in_dir}")
        return 1
    rc = 0
    for f in files:
        txt = in_dir / (f.name + ".txt")
        if txt.exists() and not args.force:
            print(f"skip existing {txt}")
            continue
        rc |= transcribe_file(f, in_dir, args.language)
    transcript = in_dir / "transcript.md"
    with transcript.open("w", encoding="utf-8") as out:
        out.write(f"# Meeting transcript {in_dir.name}\n\n")
        for f in files:
            txt = in_dir / (f.name + ".txt")
            if txt.exists():
                out.write(f"\n## {f.name}\n\n")
                out.write(txt.read_text(encoding="utf-8", errors="replace").strip() + "\n")
    print(f"MERGED_TRANSCRIPT: {transcript}")
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description="macOS Zoom/meeting recorder helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("doctor")
    p.add_argument("--test", action="store_true", help="also run short recording preflight")
    p.add_argument("--seconds", type=int, default=10)
    p.add_argument("--device", default=DEFAULT_DEVICE)
    p.add_argument("--out-dir", default=str(DEFAULT_ROOT / "preflight"))
    p.add_argument("--transcribe", action="store_true")
    p.set_defaults(func=doctor)

    p = sub.add_parser("preflight")
    p.add_argument("--seconds", type=int, default=10)
    p.add_argument("--device", default=DEFAULT_DEVICE)
    p.add_argument("--out-dir", default=str(DEFAULT_ROOT / "preflight"))
    p.add_argument("--transcribe", action="store_true")
    p.set_defaults(func=preflight)

    p = sub.add_parser("preflight-system", help="record system output via AudioTee, no BlackHole required")
    p.add_argument("--seconds", type=int, default=10)
    p.add_argument("--out-dir", default=str(DEFAULT_ROOT / "preflight"))
    p.add_argument("--transcribe", action="store_true")
    p.add_argument("--tone", action=argparse.BooleanOptionalAction, default=True, help="play an audible test tone while recording")
    p.set_defaults(func=preflight_system)

    p = sub.add_parser("record")
    p.add_argument("--device", default=DEFAULT_DEVICE)
    p.add_argument("--out-dir", default=str(DEFAULT_ROOT))
    p.add_argument("--chunk-seconds", type=int, default=300)
    p.add_argument("--duration", type=int, default=0, help="optional max duration seconds")
    p.set_defaults(func=record)

    p = sub.add_parser("record-system", help="record chunked system output via AudioTee, no BlackHole required")
    p.add_argument("--out-dir", default=str(DEFAULT_ROOT))
    p.add_argument("--chunk-seconds", type=int, default=300)
    p.set_defaults(func=record_system)

    p = sub.add_parser("transcribe")
    p.add_argument("path")
    p.add_argument("--language", default="auto")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=transcribe)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
