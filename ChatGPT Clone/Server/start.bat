@echo off
echo Starting ChatBot Server on port 8001...
cd /d "c:\Users\shanaya\Documents\CCOBJPGL_PROJECT_COM246\ChatGPT Clone\server"
taskkill /f /im python.exe 2>nul
python simple_server.py
pause
