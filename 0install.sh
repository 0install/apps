#!/bin/sh
set -e

download() {
    zeroinstall_release=0install-$(uname | tr '[:upper:]' '[:lower:]')-$(uname -m)-${ZEROINSTALL_VERSION:-latest}
    download_dir=~/.cache/0install.net/$zeroinstall_release

    if [ ! -f $download_dir/files/0install ]; then
        echo "Downloading 0install..." >&2
        rm -rf $download_dir
        mkdir -p $download_dir
        curl -sSL https://get.0install.net/$zeroinstall_release.tar.bz2 | tar xj --strip-components 1 --directory $download_dir
    fi
}

if command -v 0install > /dev/null 2> /dev/null; then
    0install "$@"
else
    download
    $download_dir/files/0install "$@"
fi
