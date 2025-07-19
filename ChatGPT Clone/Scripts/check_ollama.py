# Python script to check if Ollama is running and start it if needed
import subprocess
import sys
import time
import requests

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/version', timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Start Ollama service"""
    try:
        subprocess.Popen(['ollama', 'serve'], shell=True)
        print("Starting Ollama service...")
        time.sleep(5)  # Wait for service to start
        return True
    except:
        return False

if __name__ == "__main__":
    print("Checking Ollama status...")
    
    if check_ollama():
        print("✓ Ollama is running")
    else:
        print("✗ Ollama is not running")
        print("Attempting to start Ollama...")
        
        if start_ollama():
            if check_ollama():
                print("✓ Ollama started successfully")
            else:
                print("✗ Failed to start Ollama")
                sys.exit(1)
        else:
            print("✗ Could not start Ollama")
            sys.exit(1)
    
    print("All systems ready!")
