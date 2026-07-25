#requires -Version 5.1

<#
.SYNOPSIS
Installs or verifies Windows development tools and VS Code extensions for YTDOWN.

.DESCRIPTION
This script uses only Windows PowerShell and winget.

It does not use Linux shell commands.
It does not modify project source code.
#>

param(
  [switch]$SkipTools,
  [switch]$SkipExtensions
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Message
  )

  Write-Host ""
  Write-Host "==> $Message" -ForegroundColor Cyan
}

function Test-Command {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Name
  )

  return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Install-WingetPackage {
  param(
    [Parameter(Mandatory = $true)]
    [string]$PackageId,

    [Parameter(Mandatory = $true)]
    [string]$DisplayName
  )

  Write-Step "Installing $DisplayName"

  winget install `
    --exact `
    --id $PackageId `
    --accept-package-agreements `
    --accept-source-agreements
}

if (-not (Test-Command "winget")) {
  throw "winget is not installed. Install or update Microsoft App Installer first."
}

if (-not $SkipTools) {
  $Tools = @(
    @{
      Command = "git"
      Package = "Git.Git"
      Name    = "Git"
    },
    @{
      Command = "code"
      Package = "Microsoft.VisualStudioCode"
      Name    = "Visual Studio Code"
    },
    @{
      Command = "node"
      Package = "OpenJS.NodeJS.LTS"
      Name    = "Node.js LTS"
    },
    @{
      Command = "python"
      Package = "Python.Python.3.12"
      Name    = "Python 3.12"
    },
    @{
      Command = "docker"
      Package = "Docker.DockerDesktop"
      Name    = "Docker Desktop"
    },
    @{
      Command = "terraform"
      Package = "Hashicorp.Terraform"
      Name    = "Terraform"
    },
    @{
      Command = "kubectl"
      Package = "Kubernetes.kubectl"
      Name    = "kubectl"
    },
    @{
      Command = "aws"
      Package = "Amazon.AWSCLI"
      Name    = "AWS CLI"
    }
  )

  foreach ($Tool in $Tools) {
    if (Test-Command $Tool.Command) {
      Write-Host "$($Tool.Name) is already available." -ForegroundColor Green
    }
    else {
      try {
        Install-WingetPackage `
          -PackageId $Tool.Package `
          -DisplayName $Tool.Name
      }
      catch {
        Write-Warning "Could not install $($Tool.Name): $($_.Exception.Message)"
      }
    }
  }
}

if (-not $SkipExtensions) {
  if (-not (Test-Command "code")) {
    Write-Warning "The VS Code command is not available in this terminal."
    Write-Warning "Restart PowerShell after installing VS Code, then run this script again with -SkipTools."
  }
  else {
    $Extensions = @(
      "blackboxapp.blackbox",
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode",
      "bradlc.vscode-tailwindcss",
      "ms-python.python",
      "ms-python.vscode-pylance",
      "charliermarsh.ruff",
      "ms-azuretools.vscode-docker",
      "ms-vscode-remote.remote-containers",
      "redhat.vscode-yaml",
      "hashicorp.terraform",
      "ms-kubernetes-tools.vscode-kubernetes-tools",
      "github.vscode-github-actions",
      "github.vscode-pull-request-github",
      "editorconfig.editorconfig"
    )

    Write-Step "Installing VS Code extensions"

    foreach ($Extension in $Extensions) {
      try {
        code `
          --install-extension $Extension `
          --force
      }
      catch {
        Write-Warning "Could not install extension $Extension"
      }
    }
  }
}

Write-Step "Verifying commands"

$Checks = @(
  @{ Name = "Git"; Command = "git --version" },
  @{ Name = "Python"; Command = "python --version" },
  @{ Name = "Node"; Command = "node --version" },
  @{ Name = "npm"; Command = "npm --version" },
  @{ Name = "Docker"; Command = "docker --version" },
  @{ Name = "Docker Compose"; Command = "docker compose version" },
  @{ Name = "Terraform"; Command = "terraform version" },
  @{ Name = "kubectl"; Command = "kubectl version --client" },
  @{ Name = "AWS CLI"; Command = "aws --version" },
  @{ Name = "Blackbox"; Command = "blackbox --version" }
)

foreach ($Check in $Checks) {
  Write-Host ""
  Write-Host "[$($Check.Name)]" -ForegroundColor Yellow

  try {
    Invoke-Expression $Check.Command
  }
  catch {
    Write-Warning "$($Check.Name) is not available in this terminal."
  }
}

Write-Host ""
Write-Host "Tool setup finished." -ForegroundColor Green
Write-Host "Restart PowerShell if newly installed commands are unavailable."
Write-Host "Start Docker Desktop manually before Docker validation."

