#!/bin/bash
set -eux
wget --quiet http://repo.roscidus.com/archives.db
0install run http://0install.net/tools/0repo.xml
