$ErrorActionPreference='Stop'
$env:PYTHONIOENCODING='utf-8'
$env:REVERSE_CLI_CACHE_DIR='E:/ai-cache/axure-pilot/cache'
$taskPython=if($env:REVERSE_CLI_PYTHON){$env:REVERSE_CLI_PYTHON}else{'E:/Runtimes/python312-3.12.14/python.exe'}
& $taskPython (Join-Path $PSScriptRoot 'axure_cli.py') @args
exit $LASTEXITCODE
