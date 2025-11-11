# Auto-update script for GitHub
Write-Host "Updating GitHub repository..." -ForegroundColor Cyan
Set-Location $PSScriptRoot

git add .
git commit -m "Auto-update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSuccessfully pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host "`nPush failed. You may need to pull first with: git pull origin main" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit"

