#!/bin/bash

chrome_path="/Applications/Google Chrome.app"

cd ~/Apps/Builds/lute-v3/
source .venv/bin/activate
python -m lute.main --port 9876 &
sleep 1
open -a "$chrome_path" --args "http://localhost:9876"