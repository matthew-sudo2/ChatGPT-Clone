#!/usr/bin/env python3
"""Test script to check Ollama API directly"""

import requests
import json

def test_ollama_api():
    try:
        # Test the generate endpoint with gemma3
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "gemma3",
            "prompt": "Hello, how are you?",
            "stream": False
        }
        
        print("Testing Ollama API...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ API call successful!")
            print(f"Response: {result.get('response', 'No response field')}")
            return True
        else:
            print(f"✗ API call failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Exception occurred: {e}")
        return False

def test_available_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            print("Available models:")
            for model in models.get('models', []):
                print(f"  - {model['name']} ({model['size']} bytes)")
            return models
        else:
            print(f"Failed to get models: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting models: {e}")
        return None

if __name__ == "__main__":
    print("=== Ollama API Test ===")
    
    # Test available models
    test_available_models()
    print()
    
    # Test API call
    test_ollama_api()
