---
# YTDOWN Source and Media Task

## Milestone

Choose one only:

* source integration audit
* source-inspection API
* worker yt-dlp probe
* direct media downloader
* WebP worker integration
* frontend source recognition
* frontend conversion controls
* security hardening
* source-media documentation

## Goal

One measurable result only.

## Required Reading

* .blackbox\PROJECT_STATE.md
* .blackbox\FEATURE_SOURCE_MEDIA_STATE.md
* .blackbox\skills\ytdown-core\SKILL.md
* .blackbox\skills\ytdown-source-intelligence\SKILL.md
* .blackbox\skills\ytdown-media-conversion\SKILL.md
* relevant application files
* relevant tests
* current Git status

## Allowed Paths

List exact files before implementation.

## Protected Paths

List all unrelated services and infrastructure.

## Existing Contract

Record:

* download endpoint:
* request model:
* task identifier:
* status endpoint:
* Celery task:
* output path:
* result format:
* polling interval:
* failure values:

## New Optional Fields

Record whether these are approved:

* convert_webp:
* webp_target:

## Security Checks

* [ ] URL scheme checked
* [ ] URL credentials rejected
* [ ] hostname normalized
* [ ] private addresses rejected
* [ ] DNS resolution checked before network operation
* [ ] redirects considered
* [ ] content length limited
* [ ] output directory confined
* [ ] filename sanitized

## Validation

Use only commands that match actual project scripts.

Backend example:

```powershell
Set-Location "E:\CODES\001\YTDOWN\backend"

python -m pytest
```

Worker example:

```powershell
Set-Location "E:\CODES\001\YTDOWN\worker"

python -m pytest
```

Frontend example:

```powershell
Set-Location "E:\CODES\001\YTDOWN\frontend"

npm run lint
npm run build
```

Repository checks:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

git diff --check
git status
```

## Stop Condition

Stop after the selected milestone passes.

Do not begin the next milestone.
Do not deploy.
Do not merge.
Do not push.

