@echo off
setlocal

echo ==================================================
echo      ISEKAI: Manga to Motion AI - Launcher
echo ==================================================

:: Check for Python
set PYTHON_CMD=python

:: Try to find Python 3.10 specifically via py launcher (Recommended for compatibility)
py -3.10 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py -3.10
    echo [INFO] Found Python 3.10. Using it for best compatibility.
) else (
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
        echo Please install Python 3.10 from python.org and tick "Add Python to PATH".
    pause
    exit /b 1
)
)

:: Check for FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] FFmpeg is not installed or not in PATH.
    echo The app will run in MOCK mode ^(no video generation^) unless FFmpeg is installed.
    echo Please download FFmpeg and add it to your PATH variable.
    echo Visit: https://ffmpeg.org/download.html
    echo.
    pause
)

:: Create Virtual Environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate Virtual Environment
call venv\Scripts\activate

:: Install Dependencies
echo [INFO] Checking dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: Run the App
echo [INFO] Starting ISEKAI...
python src/app.py

pause
