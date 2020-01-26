#!/bin/bash
set -e
cd `dirname $0`

# Prepare directory for generated feeds
if [ ! -d "../incoming" ]; then
    echo "Directory ../incoming does not exist."
    exit 1
fi
cp */*.zip ../incoming/

if [[ -v CI ]]; then
    # Only feeds not handled on Windows
    FILES="golang/go-linux.watch.py golang/go-darwin.watch.py utils/nmap.watch.py"
else
    # Exclude feeds currently not supported by 0template on Linux
    FILES=$(ls */*.watch.py | grep -v cmake | grep -v gitextensions | grep -v go-windows | grep -v jq | grep -v kotlin | grep -v libreoffice | grep -v node | grep -v vagrant | grep -v vlc)
fi

# Run watch scripts
for FILE in $FILES; do
    echo "Running $FILE"
    0install run https://apps.0install.net/0install/0watch.xml --output ../incoming $FILE || true
done
