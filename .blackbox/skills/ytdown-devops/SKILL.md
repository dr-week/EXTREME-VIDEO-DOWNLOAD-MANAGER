name: ytdown-devops
description: Completes YTDOWN Docker Compose, Kubernetes, AWS Terraform integration and GitHub Actions one validated infrastructure milestone at a time without exposing secrets or deploying automatically.

---

# YTDOWN DevOps Skill

## Purpose

Complete the remaining infrastructure in a safe order.

Required order:

1. Docker Compose
2. Kubernetes
3. Pull-request CI
4. Deployment workflow
5. README and ignore rules

Do not skip directly to Kubernetes before validating Docker Compose.

## Required Reading

Before infrastructure changes, read:

1. `.blackbox\PROJECT_STATE.md`
2. `.blackbox\WORKFLOW.md`
3. `.blackbox\skills\ytdown-core\SKILL.md`
4. `.blackbox\skills\ytdown-devops\SKILL.md`
5. `.blackbox\templates\DEVOPS_TASK_TEMPLATE.md`
6. backend Dockerfile
7. worker Dockerfile
8. frontend Dockerfile
9. application environment settings
10. Terraform configuration
11. current Git status

## Infrastructure Order

### Phase 3.6 — Docker Compose

Create local orchestration for:

* Redis
* backend
* worker
* frontend

Requirements:

* reuse existing Dockerfiles
* read actual ports from the code
* read actual environment variable names
* use service health checks where possible
* use correct Redis service hostname
* preserve existing task queue behaviour
* use named volumes only when needed
* avoid arbitrary host directory mounts
* create or update `.env.example`
* do not add real secrets

Required validation:

```powershell
docker compose config
docker compose build
docker compose up -d
docker compose ps
```

Test the real health endpoint using PowerShell only after detecting its path:

```powershell
Invoke-RestMethod `
    -Method Get `
    -Uri "http://localhost:<detected-port>/<detected-health-path>"
```

Stop services after testing:

```powershell
docker compose down
```

Do not remove volumes unless explicitly approved.

### Phase 3.7 — Kubernetes

Create resources only after Compose passes.

Minimum expected resources:

* Namespace
* ConfigMap
* Secret example or placeholder
* Redis Deployment
* Redis Service
* Backend Deployment
* Backend Service
* Worker Deployment
* Frontend Deployment
* Frontend Service

Add Ingress only when routing requirements are known.

Requirements:

* readiness probes
* liveness probes
* CPU requests
* memory requests
* conservative limits
* no real secrets
* explicit image tags
* labels and selectors that match
* no LoadBalancer service unless approved

Validation:

```powershell
kubectl apply `
    --dry-run=client `
    -f ".\k8s"
```

When Kustomize exists:

```powershell
kubectl kustomize ".\k8s"
```

Do not deploy to a cluster without explicit approval.

### Phase 3.8 — Pull-Request CI

Create a focused CI workflow.

Expected checks:

* backend dependency installation
* backend tests
* worker dependency installation
* worker tests
* frontend dependency installation
* frontend lint
* frontend tests where available
* frontend production build
* Docker image build validation
* Terraform format check
* Terraform initialization without backend where needed
* Terraform validation

Requirements:

* least-privilege permissions
* concurrency control
* dependency caching
* clear job names
* no deployment from pull requests
* no secrets printed

### Phase 3.8B — Deployment Workflow

Create only after CI is stable.

Requirements:

* approved branch or manual dispatch
* GitHub environment protection
* AWS OIDC when possible
* ECR authentication
* image tags based on commit SHA
* Terraform plan
* deployment approval
* no automatic `terraform apply` until approved

Do not use long-lived AWS keys when OIDC can be used.

### Phase 3.9 — Documentation

Update:

* root README
* `.gitignore`
* environment examples

README should document:

* architecture
* prerequisites
* Windows local setup
* frontend development
* backend development
* worker development
* Docker Compose
* tests
* Kubernetes dry run
* Terraform validation
* CI/CD overview
* environment variables
* troubleshooting

`.gitignore` should include:

* Python cache
* Python virtual environments
* Node modules
* frontend build output
* environment files
* downloaded media
* Terraform state
* Terraform plan files
* Terraform cache
* local Kubernetes secret files
* editor files
* operating-system files

Do not ignore:

* dependency lock files
* Dockerfiles
* Kubernetes manifests
* Terraform source
* `.env.example`
* test files

## Secret Protection

Never commit:

* `.env`
* `.env.local`
* `.env.production`
* Terraform state
* AWS keys
* Redis passwords
* real Kubernetes Secret values
* private certificates

## Deployment Protection

Do not run:

```powershell
terraform apply
terraform destroy
kubectl apply
aws ecs update-service
git push
```

without explicit user approval.

## Windows Command Policy

Use Windows PowerShell commands.

Do not give Linux shell commands such as:

* `rm`
* `cp`
* `mv`
* `cat`
* `touch`
* `grep`
* `sed`
* `awk`
* `chmod`
* `export`

Use:

* `Remove-Item`
* `Copy-Item`
* `Move-Item`
* `Get-Content`
* `New-Item`
* `Select-String`
* `$env:VARIABLE_NAME`

## Response Format

### Infrastructure Milestone

One milestone only.

### Detected Contract

Report actual ports, variables, routes and images.

### Changes

Report exact files.

### Validation

Use PASS, FAIL, BLOCKED or NOT RUN.

### Deployment Status

State explicitly whether anything was deployed.

### Stop Point

Give one next milestone only.

