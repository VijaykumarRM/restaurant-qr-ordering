@echo off
REM Restaurant QR Ordering System - Quick Start Script for Windows

cls
echo.
echo ============================================
echo   Restaurant QR Ordering System
echo   FINAL DEPLOYMENT
echo ============================================
echo.

REM Check if Python venv exists
if not exist ".venv" (
    echo [!] Virtual environment not found!
    echo [*] Installing dependencies...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r backend/requirements.txt
    echo [+] Setup complete!
)

echo.
echo [*] Starting servers...
echo.

REM Start backend in a new window (listening on all interfaces 0.0.0.0)
echo [+] Backend server starting on 0.0.0.0:8000 (LAN accessible)
start "Restaurant API Server" cmd /k "cd %CD% && .venv\Scripts\activate.bat && uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

REM Give backend time to start
timeout /t 2 /nobreak

REM Start frontend in a new window (from frontend directory)
echo [+] Frontend server starting on 0.0.0.0:5500 (LAN accessible)
start "Restaurant Frontend Server" cmd /k "cd %CD%\frontend && python -m http.server 5500 --bind 0.0.0.0"

echo.
echo ============================================
echo   SERVERS STARTED!
echo ============================================
echo.
echo Access points:
echo   Localhost only:  http://127.0.0.1:5500/admin.html
echo   LAN (your IP):   http://10.45.12.148:5500/admin.html
echo   API Docs:        http://10.45.12.148:8000/docs
echo.
echo Admin Panel Password: admin123
echo.
echo Sample customer page:
echo   http://127.0.0.1:5500/menu.html?token=test
echo.
echo To generate menu QR codes:
echo   python generate_menu_qr_samples.py
echo.
echo For LAN setup instructions:
echo   See SETUP_LAN.md
echo.
echo SERVERS RUNNING - Keep this window open!
echo.
echo Tests:
echo   .\.venv\Scripts\python -m unittest backend.test_qr_generator backend.test_order_flow
echo.
echo Press Ctrl+C in either window to stop servers.
echo ============================================
echo.

pause
