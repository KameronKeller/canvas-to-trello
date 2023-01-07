#!/usr/bin/env bash

if ! command -v sqlite3 &> /dev/null || ! command -v python3 &> /dev/null
then
    echo "SQLite3 and/or Python3 could not be found, please install before continuing."
    exit
fi

# Create and activate a virtual environment for installation of Python packages
python3 -m venv env
source env/bin/activate

# Get the setup_complete variable from the .ini config file to determine if the master setup is complete
    # -A1 means to read 1 row from the setup section.
    # tr -d ' ' means to ignore spaces
source <(grep = <(grep -A1 "\[setup\]" config.ini | tr -d " "))

if ! $setup_complete
then
    # Install required python packages
    echo "========== Install Required Packages =========="
    pip install -r requirements.txt
fi

# Run program
python3 canvastotrello.py

# Deactivate the Python virtual environment
deactivate

