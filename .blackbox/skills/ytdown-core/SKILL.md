name: ytdown-core
description: Governs safe, predictable and test-driven iteration of the YTDOWN React, FastAPI, Celery, Redis, Docker, Terraform, Kubernetes and GitHub Actions project.

---

# YTDOWN Core Skill

## Project

Project name:

EXTREME VIDEO DOWNLOADER

Repository:

E:\CODES\001\YTDOWN

Architecture:

React Frontend
-> FastAPI Backend
-> Redis Queue
-> Celery Worker
-> yt-dlp
-> File Storage

## Required Reading

Before changing project files, read:

1. `.blackbox\PROJECT_STATE.md`
2. `.blackbox\WORKFLOW.md`
3. the relevant specialist skill
4. the relevant task template
5. current Git status
6. relevant application files
7. relevant package or dependency files

## Core Behaviour

Always inspect the actual repository.

Never assume:

* frontend port
* backend port
* API base URL
* API route
* request field names
* response field names
* Celery task name
* Redis URL variable
* download directory
* Docker image names
* health endpoint
* Terraform variable names
* Kubernetes namespace

Read these details from the code.

## One-Task Rule

Work on one milestone only.

Examples of one milestone:

* improve the downloader form
* add task-status animations
* create Docker Compose
* create backend Kubernetes Deployment
* create pull-request CI
* update local setup documentation

Do not combine unrelated milestones.

## Protected Behaviour

Preserve:

* URL submission
* format selection
* quality selection
* directory selection when supported
* task dispatch
* task polling
* task status interpretation
* download processing
* error reporting
* environment-based configuration

## Protected Files

Never remove or rename legacy `main.py` unless the user explicitly approves it.

Never modify these without task-specific approval:

* backend application logic
* worker download logic
* Terraform architecture
* Kubernetes configuration
* GitHub Actions
* environment files
* credentials
* downloaded media

## Secret Safety

Never commit:

* AWS access keys
* AWS secret keys
* API tokens
* Redis passwords
* private hostnames
* production `.env` files
* Terraform state
* Kubernetes real Secret values
* private certificates

Use:

* `.env.example`
* placeholder values
* GitHub repository secrets
* GitHub environments
* AWS OIDC
* Kubernetes Secret references

## Destructive Command Protection

Do not run:

```powershell
terraform destroy
docker system prune
docker volume prune
kubectl delete namespace
git push --force
git reset --hard
Remove-Item -Recurse -Force
```

unless the user explicitly approves the exact command and target.

## Deployment Protection

Do not run:

```powershell
terraform apply
kubectl apply
aws ecs update-service
git push
```

without explicit user approval.

Validation and dry-run commands are allowed.

## Required Workflow

For every task:

1. State the selected milestone.
2. Run `git status`.
3. Inspect all relevant existing files.
4. Report detected contracts.
5. Define allowed paths.
6. Define protected paths.
7. Provide a compact implementation plan.
8. Implement only the selected milestone.
9. Run relevant validation.
10. Fix only failures caused by the task.
11. Run `git diff --check`.
12. Summarize exact files changed.
13. Stop.

## Validation Labels

Use exactly:

* PASS
* FAIL
* BLOCKED
* NOT RUN

Never claim PASS without command output.

## Response Format

### Milestone

State one task.

### Audit

Report:

* detected framework
* detected versions
* relevant files
* environment contracts
* risks

### Plan

Report:

* files to modify
* files to create
* dependency changes
* validation commands

### Changes

Report exact changes.

### Verification

Use:

Command — Status — Important result

### Git

Report:

* branch
* changed files
* diff summary
* suggested commit command

### Stop Point

Give one next task only.

Do not automatically continue.

