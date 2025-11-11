@echo off
setlocal enabledelayedexpansion
title Venom Console Installer - Latest Pre-release Page

echo ======================================
echo      Venom Console Installer
echo ======================================
echo.

:: ----- Check for Python 3.13+ -----
set PYVER=
for /f "tokens=*" %%A in ('py -3 --version 2^>nul') do set PYVER=%%A
if "%PYVER%"=="" (
  for /f "tokens=*" %%A in ('python --version 2^>nul') do set PYVER=%%A
)

if "%PYVER%"=="" (
    echo Python not detected.
    echo Opening Python download page...
    start "" "https://www.python.org/downloads/"
    timeout /t 2 /nobreak >nul
    endlocal & exit
)

echo Found Python version: %PYVER%
for /f "tokens=2 delims= " %%v in ("%PYVER%") do set VERNUM=%%v
for /f "tokens=1,2 delims=." %%a in ("%VERNUM%") do set MAJ=%%a& set MIN=%%b
if "%MAJ%"=="3" (
  if "%MIN%" LSS "13" (
    echo Python is older than 3.13. Please upgrade and re-run.
    start "" "https://www.python.org/downloads/"
    timeout /t 2 /nobreak >nul
    endlocal & exit
  )
)

:: ----- Prepare target folder -----
set VENOM_DIR=%USERPROFILE%\Downloads\venom_console
if not exist "%VENOM_DIR%" mkdir "%VENOM_DIR%"
echo Installation folder: %VENOM_DIR%
echo.

:: ----- Fetch latest pre-release JSON -----
curl -s "https://api.github.com/repos/ghostrrr-r/venom_console/releases" > "%TEMP%\releases.json"

:: ----- Find html_url of latest pre-release -----
set "RELEASE_URL="
for /f "tokens=1* delims=:" %%A in ('findstr /i /c:"\"html_url\":" "%TEMP%\releases.json"') do (
    if not defined RELEASE_URL (
        set "RELEASE_URL=%%B"
        set RELEASE_URL=!RELEASE_URL:~2,-2!
    )
)

if not defined RELEASE_URL (
    echo Failed to find latest pre-release page.
    echo Opening releases page instead...
    start "" "https://github.com/ghostrrr-r/venom_console/releases"
    timeout /t 2 /nobreak >nul
    endlocal & exit
)

echo Opening latest pre-release page in browser...
start "" "!RELEASE_URL!"

echo.
echo After downloading, save the file into:
echo   %VENOM_DIR%
echo.
echo To run the console:
echo   python "%VENOM_DIR%\venom_console.py"

:: short pause for user visibility, then clean exit (remove or set /t 0 to close immediately)
timeout /t 2 /nobreak >nul
endlocal & exit
