#!/usr/bin/env bash

if ! command -v sqlitse3 &> /dev/null || ! command -v python3 &> /dev/null
then
    echo "SQLite3 and/or Python3 could not be found, please install before continuing."
    exit
fi

# Create and activate a virtual environment for installation of Python packages
python3 -m venv env
source env/bin/activate

# Install required python packages
pip install -r requirements.txt

# Deactivate the Python virtual environment
deactivate

echo "Setup Successful"
