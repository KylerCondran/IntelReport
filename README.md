# IntelReport

Offline LLM Summary & Intelligence Extraction From Long Transcripts

IntelReport provides a small toolkit to fully offline:
- Analyze long transcripts by running `intelreport.py`, which summarizes text in chunks from the perspective of an intelligence analyst.
- Transcribe audio with [Whisper AI](https://github.com/openai/whisper) (Not Required)

<p align="center">
  <a href="https://github.com/KylerCondran/IntelReport/issues/new">Report bug</a>
  ·
  <a href="https://github.com/KylerCondran/IntelReport/issues/new">Request feature</a>
</p>

---

## Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. YOU MAY USE THIS SOFTWARE AT YOUR OWN RISK. THE USE OF THIS SOFTWARE IS THE COMPLETE RESPONSIBILITY OF THE END-USER. THE DEVELOPERS ASSUME NO LIABILITY AND ARE NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS PROGRAM.

---

## Features
- Offline transcription using Whisper AI (local/no-cloud required) (Not Required).
- Chunked summarization of long transcripts so local LLMs can handle long inputs.
- Intelligence-analyst framing: summaries and extractions tailored to analytic needs (key actors, timeline, intent, indicators, action items).

---

## Requirements
- Python 3.8+
- ffmpeg (required by Whisper AI)
- pip

Recommended (for reasonable performance):
- CUDA-enabled GPU + compatible PyTorch build (optional but speeds up Whisper AI and local LLM inference)

---

## Installation
1. Download and install [Whisper AI](https://www.youtube.com/watch?v=ABFqbY_rmEk) and prerequisites (python, pytorch, chocolatey, ffmpeg)
2. Download and install [GPT4ALL](https://www.nomic.ai/gpt4all), download a model
3. Clone the repo
```bash
git clone https://github.com/KylerCondran/IntelReport.git
```

## Usage

Three main folders:

1) Audio
- Purpose: Drop location to dump audio files for transcription, once complete they will be moved to the archive folder.

2) Output
- Purpose: Transcripts generated from Audio, once report generated from transcript they will be moved to the archive folder.

3) Reports
- Purpose: Extracted Intel Reports from long form transcripts. 

Two main scripts:

1) TranscribeAudio.ps1
- Purpose: Powershell script to engage Whisper AI to convert audio to plain text transcript
- Moves: Audio files from Audio to Audio/Archive
- Generates: Transcript text file into Output

2) AnalyzeTranscript.ps1
- Purpose: Powershell wrapper to pass transcript to the python script IntelReport.py
- Moves: Transcript files from Output to Output/Archive
- Generates: Finalized Intel Report into Reports
- This will summarize and extract intelligence insights into bullet point format, allowing you to get intel from long form multimedia in a condensed format.

IntelReport.py options:
- --model, -m NAME/PATH       : GPT4ALL LLM Model to use for analysis. (download more models from GPT4ALL application)
- --n-threads, -t COUNT       : Number of threads to use for analysis.
- --device, -d DEVICE         : Device to use for analysis, e.g. gpu, amd, nvidia, intel. Defaults to CPU.
- --sum, -s TEXT              : String of text to summarize.
- --transcript, -x NAME/PATH  : Path to transcript file to process.
- --directive, -dir NAME/PATH : Path to custom directive file.
- --file, -f NAME/PATH        : Name of file for output.

How it works (high-level):
- Splits the transcript into manageable chunks.
- Summarizes each chunk from the perspective of an intelligence analyst (actors, timeline, intent, indicators, confidence).

---

## Tips for best results
- Clean transcripts (accurate timestamps and speaker labels) improve analysis quality.
- Tune chunk size to match your LLM's context window.
- If using large Whisper AI or large LLMs, ensure you have sufficient disk, memory, and optionally GPU resources.
- Whisper AI not required but is helpful to generate transcripts from audio fully offline.
- Add speaker diarization and timestamps to the transcript if available — the analyzer can use them to produce more accurate timelines.

---

## Contributing
See our contributing guide at [CONTRIBUTING.md](../master/CONTRIBUTING.md).

---

## Copyright and License
>The [MIT License](https://github.com/KylerCondran/IntelReport/blob/master/LICENSE.txt)
>
>Copyright (c) 2025 Kyler Condran
