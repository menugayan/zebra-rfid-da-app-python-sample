#!/usr/bin/env python3
"""
Simple Non-DA App Example
Runs as a standard background service without Data Analytics
"""
import time
import datetime
import sys

def log_message(message):
    """Print message with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)
    sys.stdout.flush()

def main():
    """Main loop - prints status periodically"""
    log_message("Hello World App Started")
    log_message("This is a non-DA application")
    
    counter = 0
    
    while True:
        counter += 1
        log_message(f"Hello World! Counter: {counter}")
        
        # You can do any custom logic here:
        # - Log to files
        # - Make HTTP requests
        # - Read/write files
        # - Run system commands
        # - Monitor system resources
        # - Send data to external APIs
        
        time.sleep(10)  # Print every 10 seconds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_message("App stopped by user")
    except Exception as e:
        log_message(f"Error: {e}")
        raise
