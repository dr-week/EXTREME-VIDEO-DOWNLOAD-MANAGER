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

Example:

ui/downloader-form-animation

## Windows Git Commands

Create a branch:

```powershell
git switch -c "ui/downloader-form-animation"
```

Check status:

```powershell
git status
```

Inspect changes:

```powershell
git diff
```

Check whitespace problems:

```powershell
git diff --check
```

Stage selected files:

```powershell
git add ".\frontend\src\App.jsx"
git add ".\frontend\src\components"
```

Commit:

```powershell
git commit -m "feat(ui): improve downloader interface"
```

Do not use:

```powershell
git add .
```

until environment files, downloaded media and generated infrastructure files have been verified.

## Worktree Workflow

Blackbox Worktree mode is preferred when available.

A manual Windows worktree can be created with:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

git fetch origin

git worktree add `
    "E:\CODES\001\YTDOWN-WORKTREES\ui-animation" `
    -b "ui/downloader-animation"
```

Enter the worktree:

```powershell
Set-Location "E:\CODES\001\YTDOWN-WORKTREES\ui-animation"
```

Remove it only after the branch is reviewed and merged:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

git worktree remove `
    "E:\CODES\001\YTDOWN-WORKTREES\ui-animation"
```

## Status Labels

Blackbox must use only these validation labels:

* PASS
* FAIL
* BLOCKED
* NOT RUN

## Completion Rule

Files existing does not mean the task is complete.

A task is complete only when:

* the expected functionality is implemented
* the relevant lint command passes
* the relevant tests pass where available
* the production build passes
* no unrelated files changed
* no secrets were added
* git diff --check passes
* Blackbox stops before starting another milestone

