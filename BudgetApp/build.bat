@echo off
REM Build script for Budget App on Windows

echo 🚀 Budget App Build Script
echo ==========================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not found
    echo Please install Python 3.8 or later from https://python.org
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "src\main.py" (
    echo ❌ Error: Please run this script from the project root directory
    echo    ^(The directory containing src\main.py^)
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install/upgrade dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Run the build
echo 🔨 Starting build process...
python build.py

echo ✅ Build script completed!
echo.
echo 📋 Next steps:
echo 1. Check the 'dist' folder for your executable
echo 2. Test the application before distribution
echo 3. The ZIP file contains everything needed for distribution
echo.

REM Deactivate virtual environment
call venv\Scripts\deactivate

pause