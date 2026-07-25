---
# YTDOWN Bug-Fix Task

## Problem

Describe the observed failure.

## Expected Behaviour

Describe what should happen.

## Reproduction

Provide exact Windows PowerShell commands or browser actions.

## Scope

Identify one affected service:

* frontend
* backend
* worker
* Docker Compose
* Kubernetes
* Terraform
* CI/CD

## Required Audit

Before editing:

1. run Git status
2. inspect the failing code
3. inspect relevant logs
4. reproduce the failure
5. identify the smallest likely cause
6. identify tests that should catch it

## Allowed Paths

List exact files.

## Protected Paths

List unrelated services and files.

## Fix Rules

* Do not perform an unrelated refactor.
* Do not change API contracts unless explicitly approved.
* Add or update a regression test where practical.
* Fix only the verified root cause.
* Do not hide errors.
* Do not remove validation merely to make tests pass.

## Verification

Record each command:

Command — PASS, FAIL, BLOCKED or NOT RUN

## Stop Condition

Stop after the reported bug is fixed and verified.

Do not begin cleanup or feature work.

