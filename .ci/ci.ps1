$ErrorActionPreference = "Stop"
Invoke-WebRequest http://repo.roscidus.com/archives.db -OutFile archives.db
0install run --batch --not-before 0.8 http://0install.net/tools/0repo.xml
if ($LASTEXITCODE -ne 0) {throw "Failed with exit code $LASTEXITCODE"}
