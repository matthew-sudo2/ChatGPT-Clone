@echo off
title ChatGPT Clone Server
color 0A

echo ====================================
echo    ChatGPT Clone Local Server
echo ====================================
echo.

:: Check if Ollama is running
echo [1/3] Checking Ollama status...
curl -s http://localhost:11434/api/version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama not detected. Starting Ollama...
    start "Ollama" ollama serve
    echo Waiting for Ollama to start...
    timeout /t 5 /nobreak >nul
) else (
    echo ✓ Ollama is running
)

echo.
echo [2/3] Stopping any existing servers...
taskkill /f /im python.exe 2>nul
if %errorlevel% equ 0 (
    echo ✓ Stopped existing Python processes
) else (
    echo ✓ No existing processes to stop
)

echo.
echo [3/3] Starting ChatGPT Clone Server...
cd /d "%~dp0server"

echo.
echo ====================================
echo  Server starting on port 8001
echo  
echo  Open in browser:
echo  → http://localhost:8001/chatbot.html
echo  → http://localhost:8001/index.html
echo ====================================
echo.
echo Press Ctrl+C to stop the server
echo.

python simple_server.py

echo.
echo Server stopped.
pause
