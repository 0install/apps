$ErrorActionPreference = "Stop"
pushd $PSScriptRoot

mkdir -Force ..\incoming | Out-Null
cp *\*.zip ..\incoming\

function Run-WatchScript($file) {
    echo $file
    .\0install.ps1 run --batch https://apps.0install.net/0install/0watch.xml --output ..\incoming $file
    if ($LASTEXITCODE -ne 0) {
        throw "Failed with exit code $LASTEXITCODE"
    }
}

foreach ($file in (ls -Recurse -Filter *.watch.py).FullName) {
    $header = Get-Content $file -TotalCount 1
    if (($header -eq "#os=Windows") -or (-not $header.StartsWith("#os="))) {
        try { Run-WatchScript $file }
        catch {
            Write-Warning "Failed, wait and retry once"
            Start-Sleep -Seconds 10
            Run-WatchScript $file
        }
    }
}

popd
