@echo off
REM Complete setup script for Python 3.10.11 - Voice Assistant

echo ============================================================
echo Voice Assistant - Complete Setup for Python 3.10
echo ============================================================
echo.

REM Check if Python 3.10 is available
py -3.10 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.10 not found!
    echo.
    echo Please install Python 3.10.11 from:
    echo https://www.python.org/downloads/release/python-31011/
    echo.
    pause
    exit /b 1
)

echo Found Python 3.10
py -3.10 --version
echo.

REM Remove old venv if exists
if exist "venv" (
    echo Removing old virtual environment...
    rmdir /s /q venv
)

REM Create new venv with Python 3.10
echo Creating virtual environment with Python 3.10...
py -3.10 -m venv venv
echo.

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
echo.

REM Install dependencies
echo Installing dependencies (this will take 5-10 minutes)...
echo Please be patient - TTS models are large...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.

REM Create .env if not exists
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env >nul
    echo.env file created (using local mode by default)
    echo.
)

REM Create directories
echo Creating directories...
if not exist "models" mkdir models
if not exist "temp" mkdir temp
echo.

echo ============================================================
echo Running verification tests...
echo ============================================================
echo.
python verify_setup.py

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo To start the voice assistant:
echo   python main.py
echo.
echo The assistant will:
echo   - Listen to your voice
echo   - Detect language automatically
echo   - Respond in the same language
echo   - Work completely offline (no API keys needed)
echo.
pause
