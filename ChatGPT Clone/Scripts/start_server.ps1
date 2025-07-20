# PowerShell script to start the chat server
Write-Host "Starting ChatGPT Clone Server..." -ForegroundColor Green

# Change to the server directory
cd "$(Split-Path -Parent $PSScriptRoot)\server"

# Start the server
python simple_server.py
