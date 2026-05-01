@echo off
title AlphaVox Installer — The Christman AI Project
color 0B
setlocal EnableDelayedExpansion

echo.
echo  =====================================================
echo   AlphaVox — One-Click Installer
echo   Voice for the Voiceless
echo   The Christman AI Project / Luma Cognify AI
echo  =====================================================
echo.

:: ── Find where this bat file lives ────────────────────────────
set "INSTALL_DIR=%~dp0"
set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"
echo  Installing from: %INSTALL_DIR%
echo.

:: ── Check Python ──────────────────────────────────────────────
echo  [1/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Python not found! Opening download page...
    echo  Install Python 3.11 or higher.
    echo  IMPORTANT: Check "Add Python to PATH" during install!
    start https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  Python !PYVER! found!

:: ── Check Node.js ─────────────────────────────────────────────
echo.
echo  [2/6] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Node.js not found! Opening download page...
    echo  Install Node.js v18 or higher.
    start https://nodejs.org/
    pause
    exit /b 1
)
for /f %%v in ('node --version 2^>^&1') do set NODEVER=%%v
echo  Node.js !NODEVER! found!

:: ── Create Python virtual environment ─────────────────────────
echo.
echo  [3/6] Setting up Python environment...
if not exist "%INSTALL_DIR%\venv" (
    python -m venv "%INSTALL_DIR%\venv"
    echo  Virtual environment created!
) else (
    echo  Virtual environment already exists — skipping.
)

:: ── Install Python packages ───────────────────────────────────
echo.
echo  [4/6] Installing Python packages (this may take a few minutes)...
call "%INSTALL_DIR%\venv\Scripts\activate.bat"
pip install --upgrade pip --quiet
pip install -r "%INSTALL_DIR%\backend\requirements.txt" --quiet
if errorlevel 1 (
    echo.
    echo  Some packages failed. Trying again...
    pip install -r "%INSTALL_DIR%\backend\requirements.txt"
)
echo  Python packages installed!

:: ── Install Node packages ─────────────────────────────────────
echo.
echo  [5/6] Installing frontend packages...
cd /d "%INSTALL_DIR%\frontend"
if not exist "node_modules" (
    call npm install --silent
    echo  Frontend packages installed!
) else (
    echo  Frontend packages already installed — skipping.
)
cd /d "%INSTALL_DIR%"

:: ── Setup .env ────────────────────────────────────────────────
echo.
echo  [6/6] Setting up configuration...
if not exist "%INSTALL_DIR%\backend\.env" (
    if exist "%INSTALL_DIR%\backend\.env.example" (
        copy "%INSTALL_DIR%\backend\.env.example" "%INSTALL_DIR%\backend\.env" >nul
        echo  Config file created from template.
        echo.
        echo  ============================================
        echo   ACTION NEEDED:
        echo   Your .env config file will open in Notepad.
        echo   Fill in your:
        echo     - AWS_ACCESS_KEY_ID
        echo     - AWS_SECRET_ACCESS_KEY
        echo     - DB_HOST (your RDS endpoint)
        echo     - DB_PASSWORD
        echo   Then save and close Notepad.
        echo  ============================================
        echo.
        pause
        notepad "%INSTALL_DIR%\backend\.env"
    )
) else (
    echo  Config already exists — keeping your settings.
)

:: ── Create desktop launcher ───────────────────────────────────
echo.
echo  Creating desktop shortcut...

set "LAUNCHER=%INSTALL_DIR%\LAUNCH_ALPHAVOX.bat"

(
echo @echo off
echo title AlphaVox
echo color 0B
echo setlocal
echo set "DIR=%INSTALL_DIR%"
echo echo.
echo echo  Starting AlphaVox...
echo echo.
echo echo  Starting backend...
echo start "AlphaVox Backend" cmd /k "cd /d !DIR! ^&^& call venv\Scripts\activate ^&^& cd backend ^&^& python wait_for_db.py --timeout 10 2^>nul ^| echo Checking DB... ^&^& cd /d !DIR! ^&^& python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"
echo timeout /t 5 /nobreak ^>nul
echo echo  Starting frontend...
echo start "AlphaVox Frontend" cmd /k "cd /d !DIR!\frontend ^&^& npm run dev"
echo timeout /t 6 /nobreak ^>nul
echo echo  Opening browser...
echo start http://localhost:5173
echo echo.
echo echo  AlphaVox is running!
echo echo  Close this window to keep it running in background.
echo echo.
echo pause
) > "%LAUNCHER%"

:: Create desktop shortcut via PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ws = New-Object -ComObject WScript.Shell; ^
     $s = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\AlphaVox.lnk'); ^
     $s.TargetPath = '%LAUNCHER%'; ^
     $s.WorkingDirectory = '%INSTALL_DIR%'; ^
     $s.Description = 'Launch AlphaVox'; ^
     $s.Save()" >nul 2>&1

echo.
echo  =====================================================
echo   AlphaVox installed successfully!
echo.
echo   A shortcut "AlphaVox" has been placed on your
echo   Desktop. Double-click it anytime to launch!
echo  =====================================================
echo.
set /p LAUNCH="  Launch AlphaVox now? (Y/N): "
if /i "!LAUNCH!"=="Y" call "%LAUNCHER%"

echo.
echo  Tech for the missing -- not the masses.
echo.
pause
