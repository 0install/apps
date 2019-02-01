$ErrorActionPreference = "Stop"
pushd $(Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)

# Ensure 0install is in the PATH
if (!(Get-Command 0install -ErrorAction SilentlyContinue)) {
    mkdir -Force "$env:TEMP\zero-install" | Out-Null
    Invoke-WebRequest "https://0install.de/files/0install.exe" -OutFile "$env:TEMP\zero-install\0install.exe"
    $env:PATH = "$env:TEMP\zero-install;$env:PATH"
}

# Exclude feeds with archives that cannot be extracted correctly on Windows
$files = (ls -Recurse -Filter *.watch.py -Exclude go-linux.watch.py,go-darwin.watch.py).FullName

foreach ($file in $files) {
    echo "Checking $file"
    cmd /c "0install run --batch http://0install.de/feeds/0watch.xml --output _watch $file 2>&1" # Redirect stderr to stdout
    if ($LASTEXITCODE -ne 0) {throw "Exit Code: $LASTEXITCODE"}
}

popd
