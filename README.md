# IntelReport

Offline LLM Summary & Intelligence Extraction From Long Transcripts

IntelReport provides a small toolkit to:
- A Script to transcribe audio files to text using Whisper AI.
- Analyze long transcripts by running `intelreport.py`, which summarizes text in chunks from the perspective of an intelligence analyst.

---

## Features
- Offline transcription using Whisper AI (local/no-cloud required).
- Chunked summarization of long transcripts so local LLMs can handle long inputs.
- Intelligence-analyst framing: summaries and extractions tailored to analytic needs (key actors, timeline, intent, indicators, action items).

---

## Requirements
- Python 3.8+
- ffmpeg (required by Whisper)
- pip

Recommended (for reasonable performance):
- CUDA-enabled GPU + compatible PyTorch build (optional but speeds up Whisper AI and local LLM inference)

---

## Installation

1. Clone the repo
```bash
git clone https://github.com/KylerCondran/IntelReport.git
cd IntelReport
```

## Usage

Two main scripts:

1) TranscribeAudio.ps1
- Purpose: use Whisper AI to convert audio -> plain text transcript

2) AnalyzeTranscript.ps1
- Purpose: wrapper to pass transcript to the python script IntelReport.py
- This will summarize and extract intelligence insights into bullet point format, allowing you to get intel from long form multimedia in a condensed approach.

Common options:
- --model NAME/PATH   : local LLM identifier or runtime (e.g., path to a local model or "gpt-local")

How it works (high-level):
- Splits the transcript into manageable chunks.
- Summarizes each chunk from the perspective of an intelligence analyst (actors, timeline, intent, indicators, confidence).
- Aggregates chunk summaries, deduplicates and synthesizes a final report.

---

## Tips for best results
- Clean transcripts (accurate timestamps and speaker labels) improve analysis quality.
- Tune chunk size to match your LLM's context window.
- If using large Whisper AI or large LLMs, ensure you have sufficient disk, memory, and optionally GPU resources.
- Add speaker diarization and timestamps to the transcript if available — the analyzer can use them to produce more accurate timelines.

---
