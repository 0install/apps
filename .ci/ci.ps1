$ErrorActionPreference = "Stop"

cmd /c "git clone https://github.com/0install/repo.roscidus.com.git --single-branch --branch=public --depth=1 public 2>&1" # Redirect stderr to stdout
cp public\archives.db .

$env:CI = "true"
0install run --batch http://0install.net/tools/0repo.xml
if ($LASTEXITCODE -ne 0) {throw "Failed with exit code $LASTEXITCODE"}
