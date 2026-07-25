Use the ytdown-core and ytdown-devops skills.

Read the completed Docker Compose audit.

Execute Phase 3.6 only.

Create the local Docker Compose integration from detected project contracts.

Required services:

* redis
* backend
* worker
* frontend

Requirements:

* reuse existing Dockerfiles
* use actual detected ports
* use actual detected environment variable names
* preserve API contracts
* preserve Celery contracts
* use Redis service hostname inside containers
* add health checks where supported
* add dependency conditions where supported
* use named volumes only when needed
* do not mount arbitrary personal Windows directories
* create or update .env.example without real secrets
* do not modify Kubernetes
* do not modify GitHub Actions
* do not redesign Terraform
* do not modify frontend UI
* do not modify application logic unless a verified integration bug requires it

Run:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

docker compose config
docker compose build
docker compose up -d
docker compose ps
```

Test the detected backend health route using Invoke-RestMethod.

Test one real task creation and polling flow when technically safe.

Then run:

```powershell
docker compose down
git diff --check
git status
```

Do not delete Docker volumes.
Do not deploy.
Do not merge.
Do not push.
Do not begin Kubernetes.

Stop after reporting validation output and exact files changed.

