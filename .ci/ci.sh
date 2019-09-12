#!/bin/bash
set -eux

git clone https://github.com/0install/repo.roscidus.com.git --single-branch --branch=public --depth=1 public || true
cp public/archives.db .

export CI=true
0install run http://0install.net/tools/0repo.xml
