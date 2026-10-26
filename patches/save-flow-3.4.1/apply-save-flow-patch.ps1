param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot
)

$ErrorActionPreference = 'Stop'
# In this repository the patched client file sits beside this script.
$source = Join-Path $PSScriptRoot 'ReflexAiClient.java'
$target = Join-Path $ProjectRoot 'src/main/java/com/example/reflexai/client/ReflexAiClient.java'

if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
    throw "Patch source not found: $source"
}
if (-not (Test-Path -LiteralPath $target -PathType Leaf)) {
    throw "Target source not found: $target. Make sure ProjectRoot points to the full Reflex AI project."
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backup = "$target.bak-$stamp"
Copy-Item -LiteralPath $target -Destination $backup
Copy-Item -LiteralPath $source -Destination $target -Force

Write-Host "Applied save-flow patch to: $target"
Write-Host "Previous file backed up to: $backup"
Write-Host 'This changes source only; it does not build or install a JAR.'
