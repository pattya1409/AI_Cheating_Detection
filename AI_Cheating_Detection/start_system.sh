#!/bin/bash

echo "========================================"
echo "AI Cheating Detection System Launcher"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python found. Starting system..."
echo

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start the application
python3 run_app.py