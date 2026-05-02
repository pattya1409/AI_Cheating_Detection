@echo off
echo ========================================
echo   AI Cheating Detection System v2.0
echo   Starting Application...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\activate
    echo Then: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo [2/3] Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
)

REM Start the application
echo [3/3] Starting Flask application...
echo.
echo ========================================
echo   Application Starting!
echo   URL: http://localhost:5000
echo   Login: admin / admin123
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
