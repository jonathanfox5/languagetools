#!/bin/bash

chrome_path="/Applications/Google Chrome.app"

cd ~/Apps/Builds/lute-v3/
source .venv/bin/activate
python -m lute.main --port 9876
