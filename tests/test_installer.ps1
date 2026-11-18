# Native Windows integration test. uv/Python/package installs are real; Claude is a controlled stub.
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$SandboxDir = Join-Path ([IO.Path]::GetTempPath()) ([guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $SandboxDir | Out-Null
$PreviousAppData = $env:APPDATA
$env:APPDATA = Join-Path $SandboxDir "appdata"
$ConfigPath = Join-Path $HOME ".claude.json"
if (Test-Path $ConfigPath) { throw "This test requires a disposable CI user without .claude.json" }
$global:DavinciInstallerTestFailRegistration = $false
function global:claude {
    $items = @($args)
    $config = if (Test-Path $ConfigPath) { Get-Content $ConfigPath -Raw | ConvertFrom-Json -AsHashtable } else { @{ mcpServers = @{} } }
    switch ($items[1]) {
        'get' { $global:LASTEXITCODE = if ($config.mcpServers.ContainsKey('davinci-resolve')) { 0 } else { 1 }; return }
        'remove' { $config.mcpServers.Remove('davinci-resolve') | Out-Null }
        'add' {
            if ($items -notcontains '-m' -or $items -notcontains 'davinci_mcp.server' -or $items -notcontains 'user') { throw "Wrong MCP launch command or scope" }
            $config.mcpServers['davinci-resolve'] = @{ command = 'controlled'; args = @('-m', 'davinci_mcp.server') }
        }
        default { throw "Unexpected Claude command" }
    }
    $config | ConvertTo-Json -Depth 20 | Set-Content $ConfigPath
    $global:LASTEXITCODE = if ($global:DavinciInstallerTestFailRegistration -and $items[1] -eq 'add') { 42 } else { 0 }
}
try {
    @{ unrelated = 'preserve'; mcpServers = @{ other = @{ command = 'existing' } } } | ConvertTo-Json -Depth 10 | Set-Content $ConfigPath
    $InstallDir = Join-Path $SandboxDir 'installation'
    $StartDir = Join-Path $env:APPDATA 'Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Start'
    New-Item -ItemType Directory -Path $StartDir -Force | Out-Null
    $UnrelatedScript = Join-Path $StartDir 'autostart.py'
    Set-Content $UnrelatedScript '# personal autostart must survive'
    $OriginalScriptHash = (Get-FileHash $UnrelatedScript).Hash

    & "$RepoRoot/scripts/install.ps1" -InstallDir $InstallDir -WhatIf
    if (Test-Path $InstallDir) { throw 'WhatIf wrote an installation' }
    & "$RepoRoot/scripts/install.ps1" -InstallDir $InstallDir -EnableAutostart -Confirm:$false
    $Python = Join-Path $InstallDir '.venv\Scripts\python.exe'
    & $Python -c 'import davinci_mcp.server'
    if ($LASTEXITCODE -ne 0) { throw 'Installed import failed' }
    $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json -AsHashtable
    if ($config.unrelated -ne 'preserve' -or $config.mcpServers.other.command -ne 'existing') { throw 'Unrelated configuration changed' }
    $Sentinel = Join-Path $InstallDir 'preserve-on-rollback.txt'
    Set-Content $Sentinel 'old installation'
    $BeforeFailure = [Convert]::ToBase64String([IO.File]::ReadAllBytes($ConfigPath))
    $BridgePath = Join-Path $env:APPDATA 'Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\CursorBridge.py'
    $BridgeHash = (Get-FileHash $BridgePath).Hash
    $global:DavinciInstallerTestFailRegistration = $true
    $Failed = $false
    try { & "$RepoRoot/scripts/install.ps1" -InstallDir $InstallDir -Force -EnableAutostart -Confirm:$false } catch { $Failed = $true }
    if (-not $Failed) { throw 'Injected registration failure was ignored' }
    if (-not (Test-Path $Sentinel)) { throw 'Previous environment was not restored' }
    if ([Convert]::ToBase64String([IO.File]::ReadAllBytes($ConfigPath)) -ne $BeforeFailure) { throw 'Configuration rollback was not byte exact' }
    if ((Get-FileHash $BridgePath).Hash -ne $BridgeHash) { throw 'Bridge rollback failed' }
    $global:DavinciInstallerTestFailRegistration = $false
    $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json -AsHashtable
    $config.mcpServers['davinci-resolve']['env'] = @{ CUSTOM_SETTING = 'preserve' }
    $config | ConvertTo-Json -Depth 20 | Set-Content $ConfigPath
    & "$RepoRoot/scripts/install.ps1" -InstallDir $InstallDir -Force -Confirm:$false
    $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json -AsHashtable
    if ($config.mcpServers['davinci-resolve'].env.CUSTOM_SETTING -ne 'preserve') { throw 'Server environment was lost on upgrade' }
    if ((Get-FileHash $UnrelatedScript).Hash -ne $OriginalScriptHash) { throw 'Unrelated startup script was overwritten' }
    if (-not (Get-ChildItem "$InstallDir.backup-*" -Directory)) { throw 'Upgrade backup missing' }
    Write-Host 'PASS: WhatIf, real installation, update, injected rollback, unrelated config and autostart preservation'
} finally {
    $env:APPDATA = $PreviousAppData
    Remove-Item Function:\claude -ErrorAction SilentlyContinue
    if (Test-Path $ConfigPath) { Remove-Item $ConfigPath }
}
