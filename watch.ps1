pushd $PSScriptRoot

if (-not (Test-Path "..\incoming" -PathType Container)) {
    throw "Directory ..\incoming does not exist."
}
cp *\*.zip ..\incoming\

foreach ($file in (ls -Recurse -Filter *.watch.py).FullName) {
    $header = Get-Content $file -TotalCount 1
    if (($header -eq "#os=Windows") -or (-not $header.StartsWith("#os="))) {
        echo $file
        #.\0install.ps1 run --batch https://apps.0install.net/0install/0watch.xml --output ..\incoming $file
        .\0install.ps1 run --batch 0watch-windows.xml.selections --output ..\incoming $file
    }
}

popd
