import http.server
import socketserver
import json
import subprocess
import os
import sys

PORT = 8001  # Changed port to avoid conflicts

class ChatBotHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Add cache-busting headers for CSS and JS files
        if self.path.endswith(('.css', '.js')):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/chat':
            self.handle_chat()
        else:
            super().do_POST()
    
    def handle_chat(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            prompt = data.get('message', 'Hello')
            image_data = data.get('image', None)  # Base64 encoded image
            print(f"Received message: {prompt}")  # Debug logging
            if image_data:
                print("Image data received for vision analysis")  # Debug logging
            
            # Try to run ollama via API
            try:
                import urllib.request
                import urllib.parse
                
                # Prepare Ollama API request
                if image_data:
                    # For vision requests with image
                    ollama_data = {
                        "model": "gemma3:latest",
                        "prompt": prompt + "\n\nIMPORTANT: Stay focused on the current topic. Maintain conversation context. Don't shift topics unless the user explicitly asks for something different.",
                        "images": [image_data],  # Base64 image
                        "stream": False,
                        "options": {
                            "temperature": 0.7,  # Lower temperature for more focused responses
                            "top_p": 0.9,
                            "repeat_penalty": 1.1
                        }
                    }
                else:
                    # For text-only requests
                    ollama_data = {
                        "model": "gemma3:latest",
                        "prompt": prompt + "\n\nIMPORTANT: Stay focused on the current topic. Maintain conversation context. Don't shift topics unless the user explicitly asks for something different.",
                        "stream": False,
                        "options": {
                            "temperature": 0.7,  # Lower temperature for more focused responses
                            "top_p": 0.9,
                            "repeat_penalty": 1.1
                        }
                    }
                
                req = urllib.request.Request(
                    'http://localhost:11434/api/generate',
                    data=json.dumps(ollama_data).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=60) as response:  # Increased timeout for vision
                    result = json.loads(response.read().decode('utf-8'))
                    ai_response = result.get('response', 'No response from AI')
                    print(f"Ollama API response: {ai_response}")  # Debug logging
                    
            except Exception as api_error:
                print(f"Ollama API failed: {api_error}")  # Debug logging
                # Fallback to command line
                try:
                    result = subprocess.run(
                        ['ollama', 'run', 'gemma3:latest', prompt],
                        capture_output=True,
                        text=True,
                        timeout=30,
                        shell=True
                    )
                    
                    if result.returncode == 0:
                        ai_response = result.stdout.strip()
                        print(f"Command line response: {ai_response}")  # Debug logging
                    else:
                        ai_response = f"Command failed: {result.stderr}"
                        print(f"Command failed: {result.stderr}")  # Debug logging
                        
                except Exception as cmd_error:
                    ai_response = f"Both API and command failed. API error: {api_error}. Command error: {cmd_error}"
                    print(f"Both methods failed: {cmd_error}")  # Debug logging
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': ai_response}).encode())
            
        except Exception as e:
            print(f"Server error: {e}")  # Debug logging
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

if __name__ == "__main__":
    # Set working directory to Public folder for serving static files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    public_dir = os.path.join(script_dir, '..', 'Public')
    
    # Check if Public folder exists, fallback to public (lowercase)
    if not os.path.exists(public_dir):
        public_dir = os.path.join(script_dir, '..', 'public')
    
    print(f"Serving files from: {public_dir}")
    os.chdir(public_dir)
    
    with socketserver.TCPServer(("", PORT), ChatBotHandler) as httpd:
        print(f"ChatBot server running at http://localhost:{PORT}/")
        print(f"Open http://localhost:{PORT}/chatbot.html in your browser")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
