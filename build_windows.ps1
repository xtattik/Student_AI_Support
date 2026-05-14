# Build StudentAI for Windows
# Run from the project root in your virtual environment:
#   .venv\Scripts\activate
#   .\build_windows.ps1

Set-StrictMode -Off

Write-Host "=== Student AI Support — Windows Build ===" -ForegroundColor Cyan

# Ensure llamafile binary exists
if (-not (Test-Path "bin\llamafile.exe")) {
    Write-Host "Downloading llamafile binary..." -ForegroundColor Yellow
    python download_llamafile.py
}

# Clean previous build
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

# Run PyInstaller
Write-Host "Running PyInstaller..." -ForegroundColor Yellow
pyinstaller student_ai.spec

if (-not $?) {
    Write-Host "PyInstaller failed." -ForegroundColor Red
    exit 1
}

# Create models folder in dist (students download model on first run)
New-Item -ItemType Directory -Force "dist\StudentAI\models" | Out-Null

# Zip it up
Write-Host "Creating zip archive..." -ForegroundColor Yellow
$version = Get-Date -Format "yyyy-MM-dd"
Compress-Archive -Path "dist\StudentAI" -DestinationPath "StudentAI-Windows-$version.zip" -Force

Write-Host ""
Write-Host "Done! Distribute: StudentAI-Windows-$version.zip" -ForegroundColor Green
Write-Host "Students unzip it and double-click StudentAI.exe" -ForegroundColor Green
