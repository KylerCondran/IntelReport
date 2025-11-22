$scriptPath = $PSScriptRoot

function Transcribe-Audio($filePath) {
	whisper "$filePath" --model small.en --output_dir "$scriptPath\output" --output_format txt
	Move-Item -Path "$filePath" -Destination "$scriptPath\audio\archive"
}

Get-ChildItem -Path "$scriptPath\audio\" -Filter *.mp3 -File -ErrorAction SilentlyContinue | ForEach-Object {
	Write-Host $_.FullName -ForegroundColor Yellow
	Transcribe-Audio($_.FullName)
}

Write-Host Done. -ForegroundColor Yellow