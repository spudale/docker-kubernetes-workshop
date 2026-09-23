$ErrorActionPreference = "Stop"

$commands = @("docker", "kubectl", "kind", "python", "git")
$results = foreach ($command in $commands) {
    $resolved = Get-Command $command -ErrorAction SilentlyContinue
    [pscustomobject]@{
        Tool = $command
        Installed = [bool]$resolved
        Path = if ($resolved) { $resolved.Source } else { "" }
    }
}

$results | Format-Table -AutoSize

if ($results.Installed -contains $false) {
    throw "Install the missing workshop tools."
}

docker version | Out-Null
docker info | Out-Null
kubectl cluster-info | Out-Null
python --version
docker compose version
kind version
kubectl get nodes

Write-Host "Workshop preflight passed." -ForegroundColor Green
