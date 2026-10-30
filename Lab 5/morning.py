import argparse
import json
import subprocess
import sys
from datetime import datetime

import requests

# Fix Unicode printing over SSH
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

parser = argparse.ArgumentParser()
parser.add_argument("--log", default="doomscroll_log.jsonl")
parser.add_argument("--model", default="qwen3.5:0.8b")
parser.add_argument(
    "--voice-model",
    default=f"{str((__import__('pathlib').Path.home() / 'Documents/GitHub/Interactive-Lab-Hub/Lab 3/speech-scripts/en_US-lessac-medium.onnx'))}",
)
parser.add_argument("--wav-out", default="morning_report.wav")
args = parser.parse_args()

with open(args.log, encoding="utf-8") as f:
    entries = [json.loads(line) for line in f if line.strip()]

# Keep only completed phone sessions
sessions = [e for e in entries if e.get("event") == "phone_session_end"]
doomscroll_sessions = [e for e in sessions if e.get("doomscrolling", False)]
total_minutes = sum(e.get("duration_minutes", 0) for e in sessions)

def format_time(epoch):
    return datetime.fromtimestamp(epoch).strftime("%I:%M %p")

print(f"Total phone sessions: {len(sessions)}")
print(f"Total phone use: {total_minutes:.1f} minutes")
print(f"Doomscrolling sessions: {len(doomscroll_sessions)}")

if not sessions:
    report = "Good morning. No completed phone sessions were recorded last night."
    print("\nMorning Report:\n")
    print(report)
else:
    digest = "\n".join(
        f"Phone use from {format_time(e['start_epoch'])} "
        f"to {format_time(e['end_epoch'])}, "
        f"duration {e['duration_minutes']:.1f} minutes, "
        f"doomscrolling: {e['doomscrolling']}"
        for e in sessions
    )

    prompt = f"""
You are a playful bedside companion giving a morning report.

Here is last night's phone-use data:

{digest}

Write a warm, slightly playful three-sentence morning report.
Include:
- how much time was spent using the phone
- whether any doomscrolling was detected
- one interesting observation about the night's behavior

Only use facts supported by the log.
Avoid judgmental language.
"""

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": args.model,
            "prompt": prompt,
            "think": False,
            "stream": False,
            "options": {"num_ctx": 4096, "temperature": 0.3},
        },
        timeout=600,
    )
    r.raise_for_status()
    report = r.json()["response"].strip()

    print("\nMorning Report:\n")
    print(report)

# Save text report
with open("morning_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

# Generate speech with Piper
subprocess.run(
    [
        "piper",
        "--model",
        args.voice_model,
        "--output_file",
        args.wav_out,
    ],
    input=report.encode("utf-8"),
    check=True,
)

# Play the audio immediately
subprocess.run(["aplay", args.wav_out], check=True)
