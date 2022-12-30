#!/usr/bin/env bash

if ! command -v sqlite3 &> /dev/null || ! command -v python3 &> /dev/null
then
    echo "SQLite3 and/or Python3 could not be found, please install before continuing."
    exit
fi

# Create and activate a virtual environment for installation of Python packages
python3 -m venv env
source env/bin/activate

# Install required python packages
pip install -r requirements.txt

# Run config setup to create config.ini to store API information
python3 config_setup.py

# Deactivate the Python virtual environment
deactivate

echo "\nSetup Successful"
