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

:: Upgrade pip and install build tools to prevent wheel building errors
echo [INFO] Upgrading pip and build tools...
python -m pip install --upgrade pip setuptools wheel cmake ninja

:: Check for C++ Compiler (cl.exe) and try to activate VS Build Tools if missing
where cl.exe >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] C++ compiler not found. Checking for VS Build Tools...
    if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
        echo [INFO] Activating VS 2022 Build Tools...
        call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
    ) else if exist "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
        echo [INFO] Activating VS 2026 Build Tools...
        call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
    ) else if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
        echo [INFO] Activating VS 2019 Build Tools...
        call "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
    ) else if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" (
        echo [INFO] Activating VS 2022 Community...
        call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
    )
)

:: Install Dependencies
echo [INFO] Checking dependencies...
pip install --prefer-binary -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    echo.
    echo [POSSIBLE FIX]
    echo It seems like your system cannot build the AI library from source.
    echo Please download and install "Visual Studio Build Tools" from Microsoft.
    echo Visit: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo Select "Desktop development with C++" during installation.
    echo.
    pause
    exit /b 1
)

:: Run the App
echo [INFO] Starting ISEKAI...
python src/app.py

pause
