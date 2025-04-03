#!/bin/bash
# Setup Python environment if needed
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies if needed
if ! pip list | grep -q pytest; then
    echo "Installing dependencies..."
    pip install -e .
fi

# Run tests
python -m pytest tests/models/test_task.py -v