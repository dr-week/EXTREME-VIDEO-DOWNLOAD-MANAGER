# YTDOWN Blackbox Setup

## Repository

```text
E:\CODES\001\YTDOWN
```

## Created Skills

### ytdown-core

General project safety, Git discipline, contract protection and validation rules.

### ytdown-visual-ui

Frontend design, responsive behaviour, accessibility and animation iteration.

### ytdown-devops

Docker Compose, Kubernetes, CI/CD and infrastructure documentation.

## Install Tools and Extensions

Open PowerShell as Administrator:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

Set-ExecutionPolicy `
    -Scope Process `
    -ExecutionPolicy Bypass `
    -Force

.\install_ytdown_dev_tools.ps1
```

Skip tool installation and install only extensions:

```powershell
.\install_ytdown_dev_tools.ps1 -SkipTools
```

Skip extensions and verify or install tools only:

```powershell
.\install_ytdown_dev_tools.ps1 -SkipExtensions
```

## Verify Blackbox Files

```powershell
Set-Location "E:\CODES\001\YTDOWN"

Get-ChildItem ".blackbox" -Recurse
```

Verify skill files:

```powershell
Get-ChildItem `
    ".blackbox\skills" `
    -Recurse `
    -Filter "SKILL.md"
```

## Restart Blackbox

Close the current Blackbox session.

Start a new session from the repository root:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

blackbox
```

Inside Blackbox, inspect discovered skills if supported:

```text
/skill list
```

## First Task: UI Audit

Copy the prompt to the Windows clipboard:

```powershell
Get-Content `
    ".blackbox\prompts\01_UI_AUDIT.md" `
    -Raw |
    Set-Clipboard
```

Paste it into Blackbox.

The audit must not modify files.

## Second Task: UI Implementation

After reviewing the audit:

```powershell
Get-Content `
    ".blackbox\prompts\02_UI_IMPLEMENT.md" `
    -Raw |
    Set-Clipboard
```

Paste it into a Blackbox Worktree session.

## Later Infrastructure Audit

After the UI work is stable:

```powershell
Get-Content `
    ".blackbox\prompts\03_DEVOPS_AUDIT.md" `
    -Raw |
    Set-Clipboard
```

## Later Docker Compose Implementation

After reviewing the infrastructure audit:

```powershell
Get-Content `
    ".blackbox\prompts\04_DEVOPS_IMPLEMENT.md" `
    -Raw |
    Set-Clipboard
```

## Git Safety

Before starting:

```powershell
git status
git branch --show-current
```

Create a UI branch:

```powershell
git switch -c "ui/downloader-interface-upgrade"
```

After Blackbox changes:

```powershell
git status
git diff
git diff --check
```

Do not stage the complete repository until generated files and environment files have been checked.

Stage selected files:

```powershell
git add ".\frontend"
git add ".\.blackbox"
```

Commit only after the frontend build passes:

```powershell
git commit -m "feat(ui): improve downloader interface and animations"
```

