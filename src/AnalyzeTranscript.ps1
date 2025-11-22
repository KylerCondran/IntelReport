$scriptPath = $PSScriptRoot
$model = "Llama-3.2-3B-Instruct-Q4_0.gguf"

function Analyze-Transcript($filePath) {
	$content = Get-Content -Path $filePath -Raw
	$fileName = [System.IO.Path]::GetFileNameWithoutExtension($filePath)
	$date = Get-Date -Format "yyyy-MM-dd-hh-mm-ss"
	$fileName = $fileName + "-" + $date
	python "$scriptPath\IntelReport.py" repl --model "$scriptPath\$model" --file "$fileName" --transcript "$filePath"
	Move-Item -Path "$filePath" -Destination "$scriptPath\output\archive"
}

Get-ChildItem -Path "$scriptPath\output\" -Filter *.txt -File -ErrorAction SilentlyContinue | ForEach-Object {
	Write-Host $_.FullName -ForegroundColor Yellow
	Analyze-Transcript($_.FullName)
}

Write-Host Done. -ForegroundColor Yellow