@echo off
REM Quick setup script for POS Minimarket on Windows
echo ========================================
echo POS Minimarket - Quick Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [1/5] Python found
python --version

REM Create virtual environment if not exists
if not exist "venv\" (
    echo.
    echo [2/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo.
    echo [2/5] Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo.
echo [3/5] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Create database if not exists
if not exist "minimarket.sqlite3" (
    echo.
    echo [4/5] Creating database...
    python create_db.py
    if errorlevel 1 (
        echo ERROR: Failed to create database
        pause
        exit /b 1
    )
) else (
    echo.
    echo [4/5] Database already exists
)

REM Run tests
echo.
echo [5/5] Running tests...
pytest tests/ -v
if errorlevel 1 (
    echo WARNING: Some tests failed
) else (
    echo All tests passed!
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To run the application:
echo   1. Double-click run.bat
echo   or
echo   2. Run: python main.py
echo.
echo Default credentials:
echo   Username: admin
echo   Password: admin123
echo.
pause
