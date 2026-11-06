$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
py -3.12 -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 is required.' }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
Write-Host 'Install Blender 4.3.2, then run .\.venv\Scripts\python.exe run.py check --blender "C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"'
