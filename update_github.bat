@echo off
echo Updating GitHub repository...
cd /d "%~dp0"
git add .
git commit -m "Auto-update: %date% %time%"
git push origin main
if %errorlevel% equ 0 (
    echo.
    echo Successfully pushed to GitHub!
) else (
    echo.
    echo Push failed. You may need to pull first with: git pull origin main
)
pause

