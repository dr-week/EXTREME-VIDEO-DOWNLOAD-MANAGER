---
# YTDOWN DevOps Task

## Milestone

Choose exactly one:

* Docker Compose audit
* Docker Compose implementation
* Kubernetes audit
* Kubernetes implementation
* pull-request CI
* deployment workflow
* README and ignore rules

## Goal

Describe one concrete infrastructure result.

## Required Reading

* `.blackbox\PROJECT_STATE.md`
* `.blackbox\WORKFLOW.md`
* `.blackbox\skills\ytdown-core\SKILL.md`
* `.blackbox\skills\ytdown-devops\SKILL.md`
* relevant Dockerfiles
* relevant application settings
* relevant Terraform files

## Allowed Paths

List exact paths.

## Protected Paths

List all unrelated application paths.

## Detected Service Contract

Record before editing:

* frontend port:
* backend port:
* backend health route:
* Redis variable:
* Celery broker variable:
* Celery result backend variable:
* download path:
* frontend API variable:
* backend image:
* worker image:
* frontend image:

## Secret Strategy

Record:

* environment example files:
* GitHub secrets:
* AWS authentication method:
* Kubernetes secret placeholders:

## Validation Commands

Use Windows PowerShell.

Example Docker Compose checks:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

docker compose config
docker compose build
docker compose up -d
docker compose ps
docker compose down
git diff --check
```

Example Kubernetes checks:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

kubectl apply `
    --dry-run=client `
    -f ".\k8s"

git diff --check
```

## Deployment Protection

Do not deploy without explicit approval.

## Stop Condition

Stop after this milestone.

Do not begin the next infrastructure phase.
Do not merge.
Do not push.

