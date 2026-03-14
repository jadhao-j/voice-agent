@echo off
REM Quick start script for Windows

echo ================================
echo Voice Assistant - Quick Setup
echo ================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies (this may take several minutes)...
echo Please wait...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Error: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo Dependencies installed
echo.

REM Create .env file
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env >nul
    echo .env file created
    echo.
    echo IMPORTANT: Edit .env and add your API keys!
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Create directories
echo Creating directories...
if not exist "models" mkdir models
if not exist "temp" mkdir temp
echo Directories created
echo.

REM Run tests
echo Running system tests...
echo.
python test_system.py

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env and add your API keys (or set LLM_PROVIDER=local)
echo 2. Run 'python main.py' to start the voice assistant
echo.
echo To activate the virtual environment in the future:
echo   venv\Scripts\activate.bat
echo.
pause
