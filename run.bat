@echo off
REM Run script for POS Minimarket

REM Check if venv exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Check if database exists
if not exist "minimarket.sqlite3" (
    echo ERROR: Database not found!
    echo Please run setup.bat first or create database with: python create_db.py
    pause
    exit /b 1
)

REM Activate virtual environment and run
echo Starting POS Minimarket...
call venv\Scripts\activate.bat
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Application exited with error
    pause
)
