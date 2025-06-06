import os
import subprocess
import sys
import time
import webbrowser
import re

def start_django_server():
    """Start the Django development server."""
    print("Starting Django server...")
    django_process = subprocess.Popen(
        ["python", "manage.py", "runserver", "0.0.0.0:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(2)  # Give the server time to start
    return django_process

def start_ngrok():
    """Start ngrok and tunnel to the Django server."""
    print("Starting ngrok tunnel...")
    ngrok_process = subprocess.Popen(
        ["ngrok", "http", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(2)  # Give ngrok time to establish the tunnel
    return ngrok_process

def get_ngrok_url():
    """Get the public ngrok URL from the ngrok API."""
    try:
        import requests
        response = requests.get("http://localhost:4040/api/tunnels")
        data = response.json()
        return data["tunnels"][0]["public_url"]
    except Exception as e:
        print(f"Error getting ngrok URL: {e}")
        print("Please check the ngrok web interface at http://localhost:4040 for your URL.")
        return None

def main():
    # Check if ngrok is installed
    try:
        subprocess.run(["ngrok", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ngrok is not installed or not in your PATH.")
        print("Please install ngrok from https://ngrok.com/download and try again.")
        return

    # Start Django server
    django_process = start_django_server()
    
    # Start ngrok
    ngrok_process = start_ngrok()
    
    # Get the ngrok URL
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        print(f"\nYour website is now available at: {ngrok_url}")
        print("Share this URL with others to access your website.")
        
        # Open the ngrok URL in the default web browser
        webbrowser.open(ngrok_url)
    
    print("\nPress Ctrl+C to stop the servers...")
    
    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        django_process.terminate()
        ngrok_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    main()
