[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "High")]
param(
    [string]$InstallDir = (Join-Path $env:LOCALAPPDATA "davinci-resolve-mcp"),
    [switch]$Force,
    [switch]$EnableAutostart
)

<#
.SYNOPSIS
    Installs this project's Python environment locally and registers the MCP
    server with Claude Code, plus (optionally) DaVinci Resolve's CursorBridge.

.DESCRIPTION
    This script assumes it is being run from a checkout of this repository
    (davinci-resolve-mcp). It does not clone anything from the network --
    the server source (src/resolve_mcp_bridge.py, src/CursorBridge.py) is
    vendored in this repo at the commit recorded in manifests/tool-manifest.json.

    Steps:
      1. Creates a Python 3.11 virtual environment under $InstallDir.
      2. Installs dependencies from requirements.lock with hash verification.
      3. Copies src/CursorBridge.py into DaVinci Resolve's Scripts/Utility
         folder and verifies the copy with a SHA-256 comparison.
      4. Registers this server with Claude Code via `claude mcp add`.
      5. Optionally enables autostart (off by default).
#>

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$LockFile = Join-Path $RepoRoot "requirements.lock"
$AutostartSource = Join-Path $RepoRoot "scripts\autostart.py"
$ServerSource = Join-Path $RepoRoot "src\resolve_mcp_bridge.py"
$BridgeSource = Join-Path $RepoRoot "src\CursorBridge.py"
$UtilityDir = Join-Path $env:APPDATA "Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"
$StartDir = Join-Path $env:APPDATA "Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Start"
$BridgeDest = Join-Path $UtilityDir "CursorBridge.py"
$AutostartDest = Join-Path $StartDir "autostart.py"
$MarkerDest = Join-Path $StartDir ".davinci-mcp-autostart-enabled"

foreach ($Command in @("uv", "claude")) {
    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Command"
    }
}
foreach ($Path in @($LockFile, $ServerSource, $BridgeSource)) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing $Path" }
}

$InstallFull = [IO.Path]::GetFullPath($InstallDir).TrimEnd('\', '/')
$InstallRoot = [IO.Path]::GetPathRoot($InstallFull).TrimEnd('\', '/')
if (-not $InstallFull -or $InstallFull -eq $InstallRoot) { throw "Unsafe InstallDir: $InstallFull" }

$ExistingMcp = $false
$PreviousErrorPreference = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
& claude mcp get davinci-resolve *> $null
$McpGetExitCode = $LASTEXITCODE
$ErrorActionPreference = $PreviousErrorPreference
if ($McpGetExitCode -eq 0) { $ExistingMcp = $true }
if (($ExistingMcp -or (Test-Path -LiteralPath $InstallFull) -or (Test-Path -LiteralPath $BridgeDest)) -and -not $Force) {
    throw "An installation of davinci-resolve-mcp, CursorBridge, or both already exists. Use -Force to back up and replace."
}

if (-not $PSCmdlet.ShouldProcess($InstallFull, "install davinci-resolve-mcp and register it with Claude Code")) {
    return
}

$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Parent = Split-Path -Parent $InstallFull
$InstallBackup = "$InstallFull.backup-$Stamp"
$BridgeBackup = Join-Path $UtilityDir ".backups\$Stamp\CursorBridge.py"

New-Item -ItemType Directory -Force -Path $Parent, $UtilityDir | Out-Null
$NewInstallPlaced = $false
$NewBridgePlaced = $false
$McpRemoved = $false
try {
    if (Test-Path -LiteralPath $InstallFull) { Move-Item -LiteralPath $InstallFull -Destination $InstallBackup }
    New-Item -ItemType Directory -Force -Path $InstallFull | Out-Null
    $NewInstallPlaced = $true

    & uv venv (Join-Path $InstallFull ".venv") --python 3.11
    if ($LASTEXITCODE -ne 0) { throw "Could not create the Python 3.11 virtual environment" }
    $Python = Join-Path $InstallFull ".venv\Scripts\python.exe"
    & uv pip install --python $Python --require-hashes --requirements $LockFile
    if ($LASTEXITCODE -ne 0) { throw "Could not install locked dependencies" }

    if (Test-Path -LiteralPath $BridgeDest) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $BridgeBackup) | Out-Null
        Move-Item -LiteralPath $BridgeDest -Destination $BridgeBackup
    }
    Copy-Item -LiteralPath $BridgeSource -Destination $BridgeDest
    $NewBridgePlaced = $true
    if ((Get-FileHash $BridgeSource -Algorithm SHA256).Hash -ne (Get-FileHash $BridgeDest -Algorithm SHA256).Hash) {
        throw "SHA-256 verification of CursorBridge failed"
    }

    if ($ExistingMcp) {
        & claude mcp remove davinci-resolve
        if ($LASTEXITCODE -ne 0) { throw "Could not remove the previous MCP registration" }
        $McpRemoved = $true
    }
    & claude mcp add --transport stdio davinci-resolve -- $Python $ServerSource
    if ($LASTEXITCODE -ne 0) { throw "Could not register davinci-resolve with Claude Code" }

    if ($EnableAutostart) {
        New-Item -ItemType Directory -Force -Path $StartDir | Out-Null
        Copy-Item -LiteralPath $AutostartSource -Destination $AutostartDest
        Set-Content -LiteralPath $MarkerDest -Value (Get-Date -Format "o") -Encoding ASCII
        Write-Warning "Autostart enabled. The bridge grants local read/write control while Resolve is open."
    } else {
        Write-Host "Autostart not enabled; start CursorBridge manually from Workspace > Scripts." -ForegroundColor Yellow
    }
} catch {
    if ($NewInstallPlaced -and (Test-Path -LiteralPath $InstallFull)) {
        Remove-Item -Recurse -Force -LiteralPath $InstallFull
    }
    if (Test-Path -LiteralPath $InstallBackup) {
        Move-Item -LiteralPath $InstallBackup -Destination $InstallFull
    }
    if ($NewBridgePlaced -and (Test-Path -LiteralPath $BridgeDest)) {
        Remove-Item -Force -LiteralPath $BridgeDest
    }
    if (Test-Path -LiteralPath $BridgeBackup) {
        Move-Item -LiteralPath $BridgeBackup -Destination $BridgeDest
    }
    Write-Warning "Installation failed; previous state was restored."
    if ($McpRemoved) {
        Write-Warning "The previous 'davinci-resolve' MCP registration was removed and not restored; re-run this script or register it manually with 'claude mcp add'."
    }
    throw
}

Write-Host "davinci-resolve-mcp installed at $InstallFull" -ForegroundColor Green
Write-Host "CursorBridge verified and installed at $BridgeDest"
if (Test-Path -LiteralPath $InstallBackup) { Write-Host "Previous install backed up at: $InstallBackup" -ForegroundColor Yellow }
if (Test-Path -LiteralPath $BridgeBackup) { Write-Host "Previous bridge backed up at: $BridgeBackup" -ForegroundColor Yellow }
& claude mcp get davinci-resolve
