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
echo "========== Install Required Packages =========="
pip install -r requirements.txt

# Run config setup to create config.ini to store API information
python3 config_setup.py

# Refresh Trello with the latest assignments from canvas
echo "Copying assignments to Trello. This may take a few minutes..."
python3 update_trello.py

# Deactivate the Python virtual environment
deactivate

echo "\nSetup Successful"
