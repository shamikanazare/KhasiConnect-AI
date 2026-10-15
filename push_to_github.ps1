[CmdletBinding()]
param(
    [string]$RepoUrl = ""
)

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "   KhasiConnect AI — Push Repository to GitHub          " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$defaultUsername = "shamikanazare"
$defaultRepoName = "KhasiConnect-AI"

if ([string]::IsNullOrWhiteSpace($RepoUrl)) {
    Write-Host "`nYour Git user configuration is set to: $defaultUsername" -ForegroundColor Gray
    $repoName = Read-Host "Enter your GitHub repository name [Press Enter for '$defaultRepoName']"
    if ([string]::IsNullOrWhiteSpace($repoName)) {
        $repoName = $defaultRepoName
    }
    
    $username = Read-Host "Enter your GitHub username [Press Enter for '$defaultUsername']"
    if ([string]::IsNullOrWhiteSpace($username)) {
        $username = $defaultUsername
    }

    $RepoUrl = "https://github.com/$username/$repoName.git"
}

Write-Host "`nConfiguring remote origin to: $RepoUrl" -ForegroundColor Yellow

# Check if origin already exists
$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Updating existing remote origin..." -ForegroundColor Gray
    git remote set-url origin $RepoUrl
} else {
    Write-Host "Adding remote origin..." -ForegroundColor Gray
    git remote add origin $RepoUrl
}

Write-Host "Pushing branch 'main' to GitHub..." -ForegroundColor Cyan
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[SUCCESS] Successfully pushed repository to GitHub!" -ForegroundColor Green
    Write-Host "Repository URL: $RepoUrl" -ForegroundColor Green
} else {
    Write-Host "`n[NOTE] If GitHub asks for authentication or if the repository does not exist yet:" -ForegroundColor Yellow
    Write-Host "1. Create an empty repository named '$repoName' on https://github.com/new (do NOT check 'Initialize with README')" -ForegroundColor White
    Write-Host "2. Then run this script again: .\push_to_github.ps1" -ForegroundColor White
}
Write-Host ""
