#!/bin/bash
set -e
cd `dirname $0`

# Set up 0repo
if [[ "$(basename $(pwd))" != "feeds" ]]; then 
  echo "This Git repo must be cloned into a directory named 'feeds' in order for 0repo to work."; exit 1
fi
cp 0repo-config.py.template ../0repo-config.py
mkdir -p ../incoming
cp */*.zip ../incoming/

# Run watch scripts
#FILES=$(ls */*.watch.py | grep -v gitextensions | grep -v go-windows | grep -v kotlin | grep -v node | grep -v vagrant | grep -v vlc) # Exclude feeds currently not supported by 0template on Linux
FILES="golang/go-linux.watch.py golang/go-darwin.watch.py" # Only feeds not handled on Windows
for FILE in $FILES; do
    echo "Running $FILE"
    0install run http://0install.de/feeds/0watch.xml --output ../incoming $FILE
done

# Merge generated feeds
cd ..
0install run --not-before 0.7 http://0install.net/tools/0repo.xml || true # Ignore error due to missing archives.db
