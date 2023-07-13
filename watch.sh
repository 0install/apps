#!/usr/bin/env bash
set -e
cd `dirname $0`

mkdir -p ../incoming
cp */*.zip ../incoming/

function run_watch_script() {
    echo $FILE
    ./0install.sh run https://apps.0install.net/0install/0watch.xml --output ../incoming $1

    # Remove downloaded archives after generating feed
    rm -f */*.zip */*.tar.gz
}

for FILE in $(ls */*.watch.py); do
    header=$(head -n 1 $FILE)
    #if [[ $header == "#os=$(uname)" ]] || [[ $header != \#os=* ]]; then
    if [[ $header == "#os=$(uname)" ]]; then
        run_watch_script $FILE || {
            echo "Failed, wait and retry once"
            sleep 10
            run_watch_script $FILE
        }
    fi
done
