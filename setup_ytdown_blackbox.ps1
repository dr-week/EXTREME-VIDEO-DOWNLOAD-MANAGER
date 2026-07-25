#requires -Version 5.1

<#
.SYNOPSIS
Creates the complete Blackbox skill structure for the existing YTDOWN project.

.DESCRIPTION
This script does not replace backend, worker, frontend, Terraform, Docker,
Kubernetes, or GitHub Actions application files.

It creates only:
- Blackbox project rules
- Blackbox skills
- task templates
- reusable prompts
- VS Code extension recommendations
- optional Windows development tools installer
- setup documentation
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = "E:\CODES\001\YTDOWN"

function Write-Section {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor DarkCyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor DarkCyan
}

function Write-Utf8File {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Content
    )

    $ParentDirectory = Split-Path -Parent $Path

    if (-not [string]::IsNullOrWhiteSpace($ParentDirectory)) {
        New-Item `
            -ItemType Directory `
            -Path $ParentDirectory `
            -Force | Out-Null
    }

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

    [System.IO.File]::WriteAllText(
        $Path,
        $Content,
        $Utf8NoBom
    )

    Write-Host "Created: $Path" -ForegroundColor Green
}

function Confirm-YtdownRepository {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Root
    )

    if (-not (Test-Path $Root)) {
        throw "Project directory does not exist: $Root"
    }

    $ExpectedDirectories = @(
        "backend",
        "worker",
        "frontend",
        "terraform"
    )

    $MissingDirectories = @()

    foreach ($Directory in $ExpectedDirectories) {
        $FullPath = Join-Path $Root $Directory

        if (-not (Test-Path $FullPath)) {
            $MissingDirectories += $Directory
        }
    }

    if ($MissingDirectories.Count -gt 0) {
        Write-Warning "Some expected directories were not found:"
        Write-Warning ($MissingDirectories -join ", ")
        Write-Warning "The setup can continue, but confirm you selected the correct YTDOWN repository."
    }

    $GitDirectory = Join-Path $Root ".git"

    if (-not (Test-Path $GitDirectory)) {
        Write-Warning "A .git directory was not found at the project root."
        Write-Warning "Confirm this is the correct Git repository before committing changes."
    }
}

Write-Section "Checking YTDOWN repository"

Confirm-YtdownRepository -Root $ProjectRoot
Set-Location $ProjectRoot

Write-Host "Project root: $ProjectRoot" -ForegroundColor Yellow

$RequiredDirectories = @(
    ".blackbox",
    ".blackbox\skills\ytdown-core",
    ".blackbox\skills\ytdown-visual-ui",
    ".blackbox\skills\ytdown-devops",
    ".blackbox\templates",
    ".blackbox\prompts",
    ".vscode"
)

Write-Section "Creating directories"

foreach ($Directory in $RequiredDirectories) {
    $FullDirectoryPath = Join-Path $ProjectRoot $Directory

    New-Item `
        -ItemType Directory `
        -Path $FullDirectoryPath `
        -Force | Out-Null

    Write-Host "Ready: $FullDirectoryPath" -ForegroundColor Green
}

# ---------------------------------------------------------------------------
# PROJECT STATE
# ---------------------------------------------------------------------------

$ProjectState = @'
# YTDOWN Project State

## Project Identity

Project name: EXTREME VIDEO DOWNLOADER

Local repository:

E:\CODES\001\YTDOWN

## Architecture

User
-> React Frontend
-> FastAPI Backend
-> Redis Queue
-> Celery Worker
-> yt-dlp
-> File Storage

## Completed Work

- [x] Phase 3.1 — Enterprise directory structure
- [x] Phase 3.2 — FastAPI backend service
- [x] Phase 3.3 — Celery and yt-dlp worker service
- [x] Phase 3.4 — React, Vite and Tailwind frontend
- [x] Phase 3.5 — Terraform AWS infrastructure

## Pending Infrastructure

- [ ] Phase 3.6 — Root Docker Compose integration
- [ ] Phase 3.7 — Kubernetes resources
- [ ] Phase 3.8 — GitHub Actions CI/CD
- [ ] Phase 3.9 — README and ignore rules

## Current Priority

Improve the existing frontend interface.

Current UI objective:

- improve visual design
- improve information hierarchy
- improve responsive behaviour
- add restrained animations
- improve task progress presentation
- improve success and failure states
- preserve all existing API behaviour

## UI Milestones

### UI-1 — Audit

- [ ] Inspect frontend package versions
- [ ] Inspect existing React structure
- [ ] Inspect Tailwind configuration
- [ ] Inspect API request and polling logic
- [ ] Identify existing animation and icon libraries
- [ ] Identify visual and accessibility problems
- [ ] Report exact files that should change

### UI-2 — Foundation

- [ ] Improve application shell
- [ ] Improve page background
- [ ] Define visual tokens
- [ ] Improve typography hierarchy
- [ ] Improve responsive spacing
- [ ] Add reusable form styles

### UI-3 — Downloader Form

- [ ] Improve URL input
- [ ] Improve format controls
- [ ] Improve quality controls
- [ ] Improve custom directory control
- [ ] Improve submit button
- [ ] Improve validation messages

### UI-4 — Task Experience

- [ ] Improve task status card
- [ ] Add processing animation
- [ ] Add completed state
- [ ] Add failure state
- [ ] Improve reset or retry interaction
- [ ] Preserve real polling state

### UI-5 — Final Verification

- [ ] Responsive browser verification
- [ ] Keyboard navigation verification
- [ ] Reduced-motion verification
- [ ] Frontend lint
- [ ] Frontend tests where available
- [ ] Frontend production build
- [ ] Git diff verification

## Protected Application Behaviour

The following must continue working:

- URL submission
- format selection
- quality selection
- custom output directory when currently supported
- backend request creation
- task ID handling
- task polling
- loading state
- completed state
- failure state
- API error display
- retry or reset behaviour
- environment-based API URL

## Protected Paths During UI Work

Do not modify these paths during UI milestones:

- backend\
- worker\
- terraform\
- k8s\
- .github\
- main.py
- database files
- downloaded media
- real environment files

## Development Rules

- Inspect before editing.
- Work on one milestone at a time.
- Use a dedicated Git branch or worktree.
- Do not merge automatically.
- Do not deploy automatically.
- Do not invent backend fields.
- Do not report PASS without command output.
- Do not start infrastructure work while a UI milestone is active.
- Update this file only after verification passes.

## Current Approved Task

Perform UI-1 audit only.

The first Blackbox run must inspect the existing frontend and must not modify files.
'@

Write-Utf8File `
    -Path (Join-Path $ProjectRoot ".blackbox\PROJECT_STATE.md") `
    -Content $ProjectState

# ---------------------------------------------------------------------------
# WORKFLOW
# ---------------------------------------------------------------------------

$Workflow = @'
# YTDOWN Blackbox Workflow

## Purpose

This workflow keeps Blackbox changes small, predictable and reviewable.

## Mandatory Development Cycle

Use this sequence for every task:

1. Inspect
2. Select one milestone
3. Define allowed paths
4. Define protected paths
5. Create or switch to a dedicated branch
6. Implement the smallest complete change
7. Run validation
8. Inspect the Git diff
9. Correct failures
10. Verify again
11. Stop
12. Review manually
13. Commit manually
14. Merge manually

## Branch Naming

Use one of these patterns:

- ui/<task-name>
- fix/<task-name>
- infra/<task-name>
- docs/<task-name>
- test/<task-name>

Example
