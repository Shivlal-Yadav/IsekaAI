@echo off
setlocal

echo ==================================================
echo      ISEKAI: Manga to Motion AI - Launcher
echo ==================================================

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from python.org and tick "Add Python to PATH".
    pause
    exit /b 1
)

:: Check for FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] FFmpeg is not installed or not in PATH.
    echo The app will run in MOCK mode (no video generation) unless FFmpeg is installed.
    echo Please download FFmpeg and add it to your PATH variable.
    echo Visit: https://ffmpeg.org/download.html
    echo.
    pause
)

:: Create Virtual Environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
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
