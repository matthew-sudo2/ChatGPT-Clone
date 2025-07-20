# Python script to check if Ollama is running and start it if needed
import subprocess
import sys
import time
import requests
import json

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/version', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_model(model_name="gemma3"):
    """Check if specific model is available"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json()
            model_names = [model['name'].split(':')[0] for model in models.get('models', [])]
            print(f"Available models: {model_names}")
            return model_name in model_names or f"{model_name}:latest" in [model['name'] for model in models.get('models', [])]
        return False
    except Exception as e:
        print(f"Error checking models: {e}")
        return False

def install_model(model_name="gemma3"):
    """Install the specified model"""
    try:
        print(f"Installing model: {model_name}...")
        print("This may take several minutes depending on model size...")
        
        # Use subprocess to run ollama pull command
        result = subprocess.run(['ollama', 'pull', model_name], 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print(f"✓ Model {model_name} installed successfully")
            return True
        else:
            print(f"✗ Failed to install model {model_name}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error installing model: {e}")
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
        
        # Check if the model is available
        print("Checking if gemma3 model is available...")
        if check_model("gemma3"):
            print("✓ gemma3 model is available")
        else:
            print("✗ gemma3 model is not available")
            print("Attempting to install gemma3 model...")
            if install_model("gemma3"):
                print("✓ gemma3 model installed successfully")
            else:
                print("✗ Failed to install gemma3 model")
                # Try alternative models
                print("Trying llama3.2 as alternative...")
                if install_model("llama3.2"):
                    print("✓ llama3.2 model installed as alternative")
                else:
                    print("✗ Failed to install alternative model")
                    sys.exit(1)
    else:
        print("✗ Ollama is not running")
        print("Attempting to start Ollama...")
        
        if start_ollama():
            if check_ollama():
                print("✓ Ollama started successfully")
                # After starting, check for model
                print("Checking for gemma3 model...")
                if not check_model("gemma3"):
                    print("Installing gemma3 model...")
                    install_model("gemma3")
            else:
                print("✗ Failed to start Ollama")
                sys.exit(1)
        else:
            print("✗ Could not start Ollama")
            sys.exit(1)
    
    print("All systems ready!")
