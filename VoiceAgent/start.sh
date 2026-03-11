#!/bin/bash

# 1. Define the cleanup function
cleanup() {
    echo -e "\nStopping sessions..."
    screen -X -S ollama quit
    screen -X -S BMO quit
    exit 0
}

# 2. Register the trap (Catch Ctrl+C / SIGINT)
trap cleanup SIGINT

# 3. Start the sessions in detached mode (-d -m)
# This allows the script to continue to the next line immediately
echo "Starting Ollama..."
screen -S ollama -d -m ollama serve

echo "Starting BMO..."
screen -S BMO -d -m python main.py

echo "Both processes are running in the background."
echo "Press Ctrl+C to terminate both screens and exit."

# 4. Keep the script alive so the trap stays active
# This waits indefinitely until you hit Ctrl+C
cat
