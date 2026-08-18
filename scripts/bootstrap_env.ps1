<#
.SYNOPSIS
    Compatibility wrapper for the pinned Phoenix SDR-DSP Windows installer.

.DESCRIPTION
    This script formerly performed rolling mlir-aie and llvm-aie installs. That
    path is retired because it bypassed the hashes and pin recorded in
    toolchain.yaml. The wrapper now delegates to install.py, the only supported
    bootstrap and repair path.

    The installer validates the XRT archive and MLIR-AIE wheel hashes, checks
    out the pinned mlir-aie revision, and does not run a silicon regression
    unless the caller explicitly requests it separately.

.PARAMETER RepoRoot
    Absolute path to the phoenix-sdr-dsp checkout. Defaults to the parent of
    this script's directory.

.PARAMETER Python
    Python command used to invoke install.py. Defaults to "python".

.EXAMPLE
    .\scripts\bootstrap_env.ps1

.EXAMPLE
    .\scripts\bootstrap_env.ps1 -RepoRoot D:\phoenix-sdr-dsp
#>

[CmdletBinding()]
param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$repo = Resolve-Path -LiteralPath $RepoRoot
$installer = Join-Path $repo "install.py"
if (-not (Test-Path -LiteralPath $installer)) {
    throw "Pinned installer not found at $installer"
}

Write-Host "Delegating to the pinned installer: $installer" -ForegroundColor Cyan
& $Python $installer --repo-root $repo
if ($LASTEXITCODE -ne 0) {
    throw "install.py failed with exit code $LASTEXITCODE"
}

Write-Host "`nPinned bootstrap/repair complete." -ForegroundColor Green
Write-Host "Run python run_all_silicon_tests.py separately on validated hardware."
