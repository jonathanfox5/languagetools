#!/bin/bash

cd ~/Apps/Builds/lute-v3/
source .venv/bin/activate
python -m lute.main --port 9876 &
sleep 1
open http://localhost:9876