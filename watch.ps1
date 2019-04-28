$ErrorActionPreference = "Stop"
pushd $PSScriptRoot

# Set up 0repo
if ((Split-Path $(pwd) -Leaf) -ne "feeds") {
  throw "This Git repo must be cloned into a directory named 'feeds' in order for 0repo to work."
}
copy 0repo-config.py.template ..\0repo-config.py
mkdir -Force ..\incoming | Out-Null
copy *\*.zip ..\incoming\

# Ensure 0install is in PATH
if (!(Get-Command 0install -ErrorAction SilentlyContinue)) {
    echo "Downloading 0install"
    mkdir -Force "$env:TEMP\zero-install" | Out-Null
    Invoke-WebRequest "https://0install.de/files/0install.exe" -OutFile "$env:TEMP\zero-install\0install.exe"
    $env:PATH = "$env:TEMP\zero-install;$env:PATH"
}

# Run watch scripts
$files = (ls -Recurse -Filter *.watch.py -Exclude go-linux.watch.py,go-darwin.watch.py).FullName # Exclude feeds with archives that cannot be extracted correctly on Windows
foreach ($file in $files) {
    echo "Running $file"
    cmd /c "0install run --batch http://0install.de/feeds/0watch.xml --output ..\incoming $file 2>&1" # Redirect stderr to stdout
    if ($LASTEXITCODE -ne 0) {throw "Failed with exit code $LASTEXITCODE"}
}

# Merge generated feeds
cd ..
cmd /c "0install run --batch --not-before 0.7 http://0install.net/tools/0repo.xml 2>&1" # Ignore error due to missing archives.db

popd
