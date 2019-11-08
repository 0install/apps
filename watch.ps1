pushd $PSScriptRoot

if ((Split-Path $(pwd) -Leaf) -ne "feeds") {
  throw "This Git repo must be cloned into a directory named 'feeds' in order for 0repo to work."
}

# Ensure 0install is in PATH
if (!(Get-Command 0install -ErrorAction SilentlyContinue)) {
    echo "Downloading 0install"
    mkdir -Force "$env:TEMP\zero-install" | Out-Null
    Invoke-WebRequest "https://0install.de/files/0install.exe" -OutFile "$env:TEMP\zero-install\0install.exe"
    $env:PATH = "$env:TEMP\zero-install;$env:PATH"
}

# Prepare directory for generated feeds
mkdir -Force ..\incoming | Out-Null
cp *\*.zip ..\incoming\

# Run watch scripts
$files = (ls -Recurse -Filter *.watch.py -Exclude go-linux.watch.py,go-darwin.watch.py,nmap.watch.py).FullName # Exclude feeds with archives that cannot be extracted correctly on Windows
foreach ($file in $files) {
    echo "Running $file"
    cmd /c "0install run --batch http://0install.de/feeds/0watch.xml --output ..\incoming $file 2>&1" # Redirect stderr to stdout
}

popd
