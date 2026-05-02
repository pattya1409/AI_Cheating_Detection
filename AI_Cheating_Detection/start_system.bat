@echo off
title AI Cheating Detection System

echo ========================================
echo AI Cheating Detection System Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Starting system...
echo.

REM Install requirements if needed
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing requirements...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Start the application
python run_app.py

pause