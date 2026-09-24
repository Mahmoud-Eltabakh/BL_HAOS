<#
.SYNOPSIS
  One-command local test runner for BL-HAOS layers.
.PARAMETER Layer
  L0 = static contracts; L1 = unit/API regression; L2 = HA SIL (Linux/WSL2 only);
  L3 = frontend unit + build + E2E; all = everything runnable on this OS.
#>
param(
    [Parameter(Position = 0)]
    [ValidateSet('L0', 'L1', 'L2', 'L3', 'all')]
    [string]$Layer = 'all'
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Bridge = Join-Path $RepoRoot 'modules\bridge'
$Integration = Join-Path $RepoRoot 'modules\integration'
$WebUi = Join-Path $Bridge 'web_ui'
$Python = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) { $Python = 'python' }

$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'

function Invoke-BridgePytest {
    & $Python -m pytest tests -q
    if ($LASTEXITCODE -ne 0) { throw "Bridge pytest failed" }
}

function Invoke-FrontendUnit {
    Push-Location $WebUi
    try { npm test; if ($LASTEXITCODE -ne 0) { throw "Frontend unit tests failed" } }
    finally { Pop-Location }
}

function Invoke-FrontendBuild {
    Push-Location $WebUi
    try { npm run build; if ($LASTEXITCODE -ne 0) { throw "Frontend build failed" } }
    finally { Pop-Location }
}

function Invoke-FrontendE2E {
    Push-Location $WebUi
    try { npm run test:e2e; if ($LASTEXITCODE -ne 0) { throw "Frontend E2E failed" } }
    finally { Pop-Location }
}

function Invoke-BridgeStatic {
    Write-Host "==> Bridge static contracts are covered inside the pytest suite" -ForegroundColor Cyan
}

function Test-IsWindowsHost {
    # Windows PowerShell 5.1 does not define $IsWindows.
    return ($PSVersionTable.PSVersion.Major -lt 6) -or $IsWindows
}

switch ($Layer) {
    'L0' {
        Push-Location $Bridge; try { Invoke-BridgeStatic } finally { Pop-Location }
        Invoke-FrontendBuild
    }
    'L1' {
        Push-Location $Bridge; try { Invoke-BridgePytest } finally { Pop-Location }
        Push-Location $Integration
        try {
            & $Python -m pytest tests/unit tests/test_package_layout.py -q -p asyncio --asyncio-mode=auto
            if ($LASTEXITCODE -ne 0) { throw "Integration unit tests failed" }
        } finally { Pop-Location }
        Invoke-FrontendUnit
    }
    'L2' {
        if ((Test-IsWindowsHost) -and $env:BLHAOS_RUN_SIL -ne '1') {
            Write-Warning "L2 (HA SIL) requires Linux or WSL2: Home Assistant Core imports fcntl. Set BLHAOS_RUN_SIL=1 inside WSL2 to override."
            exit 0
        }
        Push-Location $Integration
        try {
            $env:BLHAOS_RUN_SIL = '1'
            & $Python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto
            if ($LASTEXITCODE -ne 0) { throw "SIL suite failed" }
        } finally { Pop-Location }
    }
    'L3' {
        Invoke-FrontendUnit
        Invoke-FrontendE2E
    }
    'all' {
        Push-Location $Bridge; try { Invoke-BridgePytest } finally { Pop-Location }
        Push-Location $Integration
        try {
            & $Python -m pytest tests/unit tests/test_package_layout.py -q -p asyncio --asyncio-mode=auto
            if ($LASTEXITCODE -ne 0) { throw "Integration unit tests failed" }
        } finally { Pop-Location }
        if ((Test-IsWindowsHost) -and $env:BLHAOS_RUN_SIL -ne '1') {
            Write-Warning "Skipping L2 (HA SIL): requires Linux/WSL2 (BLHAOS_RUN_SIL=1 to override)."
        } else {
            Push-Location $Integration
            try {
                $env:BLHAOS_RUN_SIL = '1'
                & $Python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto
                if ($LASTEXITCODE -ne 0) { throw "SIL suite failed" }
            } finally { Pop-Location }
        }
        Invoke-FrontendUnit
        Invoke-FrontendBuild
    }
}

Write-Host "==> Layer '$Layer' completed successfully" -ForegroundColor Green
