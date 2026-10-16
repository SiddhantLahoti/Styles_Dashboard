@echo off
cd /d "%~dp0"
title Product Explorer - Server Engine
color 0B

echo =========================================================
echo       PRODUCT EXPLORER - STARTING SYSTEM ENGINE
echo =========================================================
echo.
echo Launching dashboard interface...

:: Browser opens immediately; frontend handles the sync screen
start "" cmd /c "timeout /t 1 >nul && start http://127.0.0.1:8000"

:: Start Uvicorn
".\python-embed\python.exe" app.py

echo.
echo [System Terminated]
pause