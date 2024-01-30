#!/usr/bin/env bash

# Get path of bash in case it's required for a user path
SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  SCRIPT_DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$SCRIPT_DIR/$SOURCE # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
SCRIPT_DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )

# User configurable paths
anki_path="/Applications/Anki.app"
lute_path="$SCRIPT_DIR/start_lute_nobrowser.sh"
lute_url="http://localhost:9876"
chrome_path="/Applications/Google Chrome.app"
asb_url="https://killergerbah.github.io/asbplayer/"
vs_path="~/Apps/Builds/vocabsieve"
deepl_path="/Applications/DeepL.app"

# Make sure python applications close when we close the terminal to give us an easy way to tidy up
trap "exit" INT TERM ERR
trap "kill 0" EXIT

# Open DeepL
open -gj -a "$deepl_path"

# Open Anki
open -gj -a "$anki_path"

# Open Lute
# eval "source \"$lute_path\" &"

# Wait prior to launching the programmes that depend on Anki
sleep 3

# Chrome (for asb player)
# open -a "$chrome_path" "$lute_url" "$asb_url"
open -a "$chrome_path" "$asb_url"

# Open vocabsieve
eval "$vs_path/.venv/bin/python $vs_path/vocabsieve.py &"

# Print a message to remind user 
sleep 3
echo "~~ This terminal is running lute and vocabsieve. Closing this terminal will also close these apps ~~"
printf "Press enter to close these scripts"
read ans
exit
