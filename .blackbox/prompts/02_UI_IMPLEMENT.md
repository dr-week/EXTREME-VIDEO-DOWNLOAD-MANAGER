Use the ytdown-core and ytdown-visual-ui skills.

Read the completed UI-1 audit before editing.

Execute one visual milestone only.

Default first target:

UI-2 application shell and downloader form foundation.

Do not perform this task unless the audit identified:

* the current React structure
* the actual API contract
* the exact frontend files
* the current dependencies
* the available npm scripts

Requirements:

* preserve all backend API behaviour
* preserve the request payload
* preserve task ID handling
* preserve polling
* preserve format options
* preserve quality options
* preserve custom directory support
* preserve success and failure behaviour
* change frontend files only
* use the existing styling system
* use the existing animation library when present
* install only one animation package when justified
* update the lock file when dependencies change
* respect prefers-reduced-motion
* provide visible keyboard focus
* maintain readable contrast
* make the layout responsive
* do not use fake progress
* do not use a background video
* do not add heavy 3D
* do not animate every element
* do not modify backend, worker, Terraform, Kubernetes or CI/CD

Required implementation cycle:

1. report current Git status
2. name one visual target
3. list exact allowed paths
4. make the change
5. run the actual frontend development server
6. inspect the result in a browser when tools permit
7. inspect the console
8. correct visible issues
9. run available lint
10. run available tests
11. run the production build
12. run git diff --check
13. summarize files changed
14. stop

Use Windows PowerShell commands only.

Do not merge.
Do not push.
Do not begin UI-4 automatically.
Do not begin infrastructure work.

