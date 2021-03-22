#!/usr/bin/env bash
set -e
cd `dirname $0`

mkdir -p ../incoming
cp */*.zip ../incoming/

for FILE in $(ls */*.watch.py); do
    header=$(head -n 1 $FILE)
    #if [[ $header == "#os=$(uname)" ]] || [[ $header != \#os=* ]]; then
    if [[ $header == "#os=$(uname)" ]]; then
        echo $FILE
        ./0install.sh run https://apps.0install.net/0install/0watch.xml --output ../incoming $FILE
    fi
done
