@echo off
title AI Cheating Detection - VS Code Runner

echo ========================================
echo AI Cheating Detection System
echo VS Code Development Runner
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Please ensure Python 3.8+ is installed
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install numpy==1.24.3
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.7
pip install flask==2.3.3
pip install werkzeug==2.3.7

REM Check if installation was successful
python -c "import flask, cv2, mediapipe; print('✓ All dependencies installed successfully!')" 2>nul
if errorlevel 1 (
    echo WARNING: Some dependencies may not be installed correctly
    echo Please check the error messages above
    pause
)

echo.
echo ========================================
echo Starting AI Cheating Detection System
echo ========================================
echo.
echo The application will start on: http://localhost:5000
echo.
echo Default Login Credentials:
echo   Admin: admin / admin123
echo   Examiner: examiner / examiner123
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

REM Run the application
python app.py

pause