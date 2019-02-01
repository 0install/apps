#!/bin/bash
set -e
cd `dirname $0`

# Exclude feeds with MSIs and with fully templated download URLs (currently not supported by 0template on Linux)
##FILES=$(ls */*.watch.py | grep -v gitextensions | grep -v go-windows | grep -v kotlin | grep -v node | grep -v vagrant)

# Only feeds that are not handled on Windows
FILES="golang/go-linux.watch.py golang/go-darwin.watch.py"

for FILE in $FILES; do
    echo "Checking $FILE"
    0install run http://0install.de/feeds/0watch.xml --output _watch $FILE
done
