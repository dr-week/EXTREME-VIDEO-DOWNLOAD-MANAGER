Use the ytdown-core and ytdown-devops skills.

Perform Phase 3.6 Docker Compose audit only.

Do not modify files.
Do not create docker-compose.yml yet.
Do not begin Kubernetes.
Do not begin CI/CD.

Inspect:

1. Git status
2. root repository structure
3. backend Dockerfile
4. backend application startup command
5. backend port
6. backend health endpoint
7. backend environment variables
8. worker Dockerfile
9. worker startup command
10. Celery application path
11. Celery broker variable
12. Celery result backend variable
13. worker output directory
14. frontend Dockerfile
15. frontend build command
16. frontend runtime port
17. frontend API environment variable
18. Redis expectations
19. storage volume requirements
20. existing environment example files
21. existing Docker network assumptions
22. existing Terraform image names
23. current tests

Return:

### Service Contract

Report actual values from the code.

### Compose Services

List the required Compose services.

### Environment Map

List each environment variable and which service uses it.

### Storage Plan

Explain which paths need persistence.

### Health Checks

List detected health endpoints and possible checks.

### Risks

List mismatches or missing configuration.

### Files Required

List exact files that Phase 3.6 should create or modify.

### Validation

Give Windows PowerShell commands only.

Stop after the audit.

