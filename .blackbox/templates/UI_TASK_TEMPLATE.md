---
# YTDOWN UI Task

## Visual Target

Choose exactly one:

* application shell
* hero
* downloader form
* URL input
* format selector
* quality selector
* custom directory control
* download button
* task status card
* progress indicator
* completed state
* failed state
* responsive layout
* animation system

## Goal

Describe one measurable visual or usability improvement.

## Required Reading

* `.blackbox\PROJECT_STATE.md`
* `.blackbox\WORKFLOW.md`
* `.blackbox\skills\ytdown-core\SKILL.md`
* `.blackbox\skills\ytdown-visual-ui\SKILL.md`
* `frontend\package.json`
* relevant frontend source files

## Allowed Paths

List exact frontend files or directories.

Example:

```text
frontend\src\App.jsx
frontend\src\components\DownloadForm.jsx
frontend\src\styles\index.css
frontend\package.json
frontend\package-lock.json
```

## Protected Paths

* backend\
* worker\
* terraform\
* k8s\
* .github\
* main.py
* real environment files

## Existing API Contract

Record before editing:

* API base URL:
* task creation route:
* HTTP method:
* request fields:
* task ID field:
* status route:
* polling interval:
* success values:
* failure values:

## Animation Plan

Record:

* element:
* trigger:
* duration:
* reduced-motion behaviour:
* library or CSS:

## Acceptance Checks

Detect scripts before running them.

```powershell
Set-Location "E:\CODES\001\YTDOWN\frontend"

npm install
npm run lint
npm run test
npm run build

Set-Location "E:\CODES\001\YTDOWN"

git diff --check
git status
```

Do not run missing npm scripts.

## Visual Checks

* [ ] Desktop layout inspected
* [ ] Tablet layout inspected
* [ ] Mobile layout inspected
* [ ] Keyboard focus inspected
* [ ] Loading state inspected
* [ ] Completed state inspected
* [ ] Failed state inspected
* [ ] Reduced motion considered
* [ ] Browser console inspected

## Stop Condition

Stop after this visual target passes validation.

Do not begin another UI milestone.
Do not begin infrastructure work.
Do not merge.

