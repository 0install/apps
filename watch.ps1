$ErrorActionPreference = "Stop"
pushd $PSScriptRoot

# Prepare directory for generated feeds
if (!(Test-Path "..\incoming" -PathType Container)) {
    throw "Directory ..\incoming does not exist."
}
cp *\*.zip ..\incoming\

# Exclude feeds with archives that cannot be extracted correctly on Windows
$files = (ls -Recurse -Filter *.watch.py -Exclude go-linux.watch.py,go-darwin.watch.py,nmap.watch.py).FullName

# Run watch scripts
foreach ($file in $files) {
    echo "Running $file"
    cmd /c "0install run --batch http://0install.de/feeds/0watch.xml --output ..\incoming $file 2>&1" # Redirect stderr to stdout
}

popd
