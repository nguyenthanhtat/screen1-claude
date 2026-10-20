# Quick installation script for Claude Code skills (Windows PowerShell)
# Usage: iwr -useb https://raw.githubusercontent.com/nguyenthanhtat/screen1-claude/main/install.ps1 | iex

Write-Host "🚀 Installing Claude Code Skills..." -ForegroundColor Cyan
Write-Host ""

# Clone repository
Write-Host "📦 Cloning repository..." -ForegroundColor Yellow
$repoPath = "$env:USERPROFILE\claude-skills"

if (Test-Path $repoPath) {
    Write-Host "⚠️  $repoPath already exists. Updating..." -ForegroundColor Yellow
    Set-Location $repoPath
    git pull origin main
} else {
    git clone https://github.com/nguyenthanhtat/screen1-claude.git $repoPath
}

# Create skills directory if it doesn't exist
$skillsPath = "$env:USERPROFILE\.claude\skills"
if (!(Test-Path $skillsPath)) {
    New-Item -ItemType Directory -Force -Path $skillsPath | Out-Null
}

# Copy skills
Write-Host "📋 Installing Test-Fully Skill..." -ForegroundColor Yellow
Copy-Item -Recurse -Force "$repoPath\skills\test-fully" "$skillsPath\"

Write-Host "📋 Installing Git Skill Suite..." -ForegroundColor Yellow
Copy-Item -Recurse -Force "$repoPath\skills\git" "$skillsPath\"

Write-Host ""
Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📖 Test your installation:" -ForegroundColor Cyan
Write-Host "   /test-fully" -ForegroundColor White
Write-Host "   /git" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation: https://github.com/nguyenthanhtat/screen1-claude" -ForegroundColor Cyan
Write-Host "📊 BigQuery skills moved to: https://github.com/nguyenthanhtat/bigquery-skills" -ForegroundColor Cyan
Write-Host ""
