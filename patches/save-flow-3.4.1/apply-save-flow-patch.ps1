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

$sourcePath = [System.IO.Path]::GetFullPath($source)
$targetPath = [System.IO.Path]::GetFullPath($target)
if ([System.StringComparer]::OrdinalIgnoreCase.Equals($sourcePath, $targetPath)) {
    throw "Patch source and target resolve to the same file; refusing to overwrite the patch."
}

$sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
$targetHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
if ($sourceHash -eq $targetHash) {
    Write-Host "The save-flow patch is already applied: $target"
    Write-Host 'No file was changed and no extra backup was created.'
    exit 0
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
$backup = "$target.bak-$stamp"
$staged = "$target.tmp-$stamp"

Copy-Item -LiteralPath $target -Destination $backup
try {
    Copy-Item -LiteralPath $source -Destination $staged
    $stagedHash = (Get-FileHash -LiteralPath $staged -Algorithm SHA256).Hash
    if ($stagedHash -ne $sourceHash) {
        throw 'Staged patch checksum did not match the source file.'
    }
    Move-Item -LiteralPath $staged -Destination $target -Force
} catch {
    if (Test-Path -LiteralPath $staged) {
        Remove-Item -LiteralPath $staged -Force
    }
    throw
}

Write-Host "Applied save-flow patch to: $target"
Write-Host "Previous file backed up to: $backup"
Write-Host 'This changes source only; it does not build or install a JAR.'
