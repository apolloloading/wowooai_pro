# Fetch Node.js LTS + pre-install agent-browser into a portable directory.
#
# Usage:
#   pwsh scripts/pack/fetch_node.ps1 -Dest <dest_dir>
#
# Pinned versions:
#   Node.js          22.14.0
#   agent-browser    0.27.0  (matches agents/skills/agent_browser-zh/SKILL.md)
#
# Why bundle:
#   `agent_browser` skill invokes `npx agent-browser@0.27.0 ...`. Windows desktop
#   users typically don't have Node on PATH; bundling avoids first-run network
#   for the CLI. Chrome for Testing is fetched by agent-browser on demand.

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$Dest
)

$ErrorActionPreference = "Stop"

$NodeVersion = "22.14.0"
$AgentBrowserVersion = "0.27.0"
$ArchSuffix = "win-x64"
$ZipName = "node-v$NodeVersion-$ArchSuffix.zip"
$Url = "https://nodejs.org/dist/v$NodeVersion/$ZipName"

if (-not (Test-Path $Dest)) {
  New-Item -ItemType Directory -Path $Dest | Out-Null
}

$Tmp = Join-Path $env:TEMP ("wowooai-node-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $Tmp | Out-Null

try {
  Write-Host "== Fetching $ZipName =="
  Invoke-WebRequest -Uri $Url -OutFile (Join-Path $Tmp $ZipName)

  Write-Host "== Extracting to $Dest =="
  Expand-Archive -Path (Join-Path $Tmp $ZipName) -DestinationPath $Tmp
  $Src = Join-Path $Tmp "node-v$NodeVersion-$ArchSuffix"
  Copy-Item -Path (Join-Path $Src "*") -Destination $Dest -Recurse -Force

  $Npm = Join-Path $Dest "npm.cmd"
  if (-not (Test-Path $Npm)) {
    throw "npm.cmd missing after extract: $Npm"
  }

  Write-Host "== Pre-installing agent-browser@$AgentBrowserVersion =="
  $env:Path = "$Dest;$env:Path"
  & $Npm install -g --prefix "$Dest" "agent-browser@$AgentBrowserVersion" 2>&1 | Out-Null
  if ($LASTEXITCODE -ne 0) {
    Write-Warning "pre-install agent-browser failed; first run will hit network"
  }

  Write-Host "== Bundled Node.js v$NodeVersion ($ArchSuffix) at $Dest =="
  Get-ChildItem $Dest | Select-Object -First 20 | Format-Table Name
}
finally {
  Remove-Item -Recurse -Force $Tmp -ErrorAction SilentlyContinue
}
