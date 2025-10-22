@echo off
REM Setup script for Valley Business Partners API Tools (Windows)

echo ========================================
echo Valley Business Partners API Tools
echo Setup Script
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo Warning: Some dependencies may not have installed correctly
    echo You may need to install them manually:
    echo   pip install -r requirements.txt
)
echo Dependencies installation complete
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy config.example.env .env >nul
    echo .env file created
    echo.
    echo IMPORTANT: Edit .env and add your API keys:
    echo   - GOOGLE_API_KEY
    echo   - OPENAI_API_KEY
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Create output directory
if not exist output (
    mkdir output
    echo output directory created
) else (
    echo output directory already exists
)
echo.

REM Run installation test
echo Running installation test...
python test_installation.py
set test_result=%errorlevel%
echo.

REM Summary
echo ========================================
echo SETUP COMPLETE
echo ========================================
echo.

if %test_result% EQU 0 (
    echo Setup successful!
    echo.
    echo Next steps:
    echo   1. Edit .env and add your API keys
    echo   2. Run the application:
    echo      venv\Scripts\activate.bat
    echo      python main.py
    echo.
    echo For help, see:
    echo   - README.md - Full documentation
    echo   - QUICKSTART.md - Quick start guide
    echo   - examples\ - Example scripts
) else (
    echo Setup completed with warnings
    echo Please check the errors above and:
    echo   1. Make sure all dependencies are installed
    echo   2. Edit .env and add your API keys
    echo   3. Run: python test_installation.py
)

echo.
echo ========================================
echo.
pause
