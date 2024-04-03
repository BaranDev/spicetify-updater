#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt install python3.10-venv
echo "Setup completed."
