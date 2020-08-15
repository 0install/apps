$ErrorActionPreference = "Stop"
Add-Type -Assembly System.Web

$workDir = "$env:TEMP\catalog-feeds"
if (Test-Path $workDir) { rm -Recurse -Force $workDir }
mkdir $workDir | Out-Null

foreach ($uri in Get-Content "$PSScriptRoot\list.txt") {
  echo $uri
  $encodedUri = [System.Web.HttpUtility]::UrlEncode($uri)
  Invoke-WebRequest $uri -OutFile "$workDir\$encodedUri"
}

0install run --command=0publish https://apps.0install.net/0install/0publish-win.xml --xmlsign --key=apps.0install.net --catalog="$PSScriptRoot\catalog.xml" "$workDir\*"

rm -Recurse -Force $workDir
