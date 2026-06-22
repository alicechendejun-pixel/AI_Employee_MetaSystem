Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is required. Install Git for Windows and reopen PowerShell."
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$vendorRoot = Join-Path $repoRoot "03_Wealth_Trading_搞钱与交易\StockTradingMaster\vendor"
$skillRoot = Join-Path $repoRoot ".claude\skills\vendor"
New-Item -ItemType Directory -Force $vendorRoot, $skillRoot | Out-Null

$sources = @(
    @{
        Name = "ai-workflow"
        Url = "https://github.com/nicepkg/ai-workflow.git"
        Paths = @(
            "workflows/stock-trader-workflow/.claude/skills/a-share-analysis",
            "workflows/stock-trader-workflow/.claude/skills/a-share-screener",
            "workflows/stock-trader-workflow/.claude/skills/akshare"
        )
    },
    @{
        Name = "claude-trading-skills"
        Url = "https://github.com/tradermonty/claude-trading-skills.git"
        Paths = @(
            "skills/us-stock-analysis",
            "skills/earnings-calendar",
            "skills/institutional-flow-tracker",
            "skills/options-strategy-advisor"
        )
    },
    @{
        Name = "Claude-Code-Stock-Deep-Research-Agent"
        Url = "https://github.com/liangdabiao/Claude-Code-Stock-Deep-Research-Agent.git"
        Paths = @(
            "1.claude/skills/stock-question-refiner",
            "1.claude/skills/stock-research-executor"
        )
    },
    @{
        Name = "claude-code-plugins-plus-skills"
        Url = "https://github.com/jeremylongshore/claude-code-plugins-plus-skills.git"
        Paths = @(
            "plugins/crypto/trading-strategy-backtester/skills/backtesting-trading-strategies"
        )
    },
    @{
        Name = "antigravity-awesome-skills"
        Url = "https://github.com/sickn33/antigravity-awesome-skills.git"
        Paths = @("skills/risk-manager")
    }
)

$installed = @()
foreach ($source in $sources) {
    $destination = Join-Path $vendorRoot $source.Name
    if (-not (Test-Path (Join-Path $destination ".git"))) {
        & git clone --depth 1 --filter=blob:none --sparse $source.Url $destination
        if ($LASTEXITCODE -ne 0) { throw "Clone failed: $($source.Name)" }
    } else {
        & git -C $destination pull --ff-only
        if ($LASTEXITCODE -ne 0) { throw "Update failed: $($source.Name)" }
    }

    & git -C $destination sparse-checkout set --no-cone @($source.Paths)
    if ($LASTEXITCODE -ne 0) { throw "Sparse checkout failed: $($source.Name)" }

    foreach ($relativePath in $source.Paths) {
        $localPath = Join-Path $destination ($relativePath -replace '/', '\')
        $skillFile = Join-Path $localPath "SKILL.md"
        if (-not (Test-Path $skillFile)) {
            Write-Warning "Missing SKILL.md: $relativePath"
            continue
        }

        $skillName = Split-Path $localPath -Leaf
        $target = Join-Path $skillRoot $skillName
        if (Test-Path $target) { Remove-Item -Recurse -Force $target }
        Copy-Item -Recurse -Force $localPath $target
        $installed += $skillName
        Write-Host "Installed $skillName" -ForegroundColor Green
    }
}

$status = [ordered]@{
    installed_at = (Get-Date).ToString("o")
    live_execution_enabled = $false
    installed_skills = $installed
}
$status | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $vendorRoot "install-status.json")

$required = @(
    "a-share-analysis",
    "us-stock-analysis",
    "stock-question-refiner",
    "stock-research-executor",
    "backtesting-trading-strategies",
    "risk-manager"
)
$missing = @($required | Where-Object { $_ -notin $installed })
if ($missing.Count -gt 0) {
    throw "Required skills missing: $($missing -join ', ')"
}

Write-Host "Stock Trading Master installation complete. Live execution remains disabled." -ForegroundColor Cyan
