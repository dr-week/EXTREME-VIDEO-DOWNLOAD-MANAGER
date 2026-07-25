Use these skills:

* ytdown-core
* ytdown-source-intelligence
* ytdown-media-conversion

Repository:

E:\CODES\001\YTDOWN

Read:

* .blackbox\PROJECT_STATE.md
* .blackbox\FEATURE_SOURCE_MEDIA_STATE.md
* .blackbox\WORKFLOW.md
* .blackbox\skills\ytdown-core\SKILL.md
* .blackbox\skills\ytdown-source-intelligence\SKILL.md
* .blackbox\skills\ytdown-media-conversion\SKILL.md
* .blackbox\templates\SOURCE_MEDIA_TASK_TEMPLATE.md

Perform a source-media integration audit only.

Do not modify files.
Do not install packages.
Do not start Docker.
Do not begin frontend redesign.

Inspect:

1. current Git branch and status
2. backend application entry
3. backend router structure
4. backend download endpoint
5. backend request models
6. backend response models
7. Celery dispatch
8. task ID handling
9. task status endpoint
10. worker Celery application
11. worker download task
12. yt-dlp options
13. final downloaded filename handling
14. download output directory
15. worker dependency manifest
16. backend dependency manifest
17. existing Pillow installation
18. existing FFmpeg expectations
19. frontend download form
20. frontend API client
21. frontend status polling
22. frontend result display
23. existing tests
24. source_recognizer.py compatibility
25. image_converter.py compatibility
26. URL security risks
27. output-path security risks
28. cookie or authentication behaviour

Return:

### Existing Contract

Give exact:

* download route
* request fields
* response fields
* task ID field
* status route
* task states
* Celery task path
* worker result format
* output directory
* frontend API environment variable

### Integration Map

Explain exactly where these should be integrated:

* source_recognizer.inspect_source
* source_recognizer.resolve_and_validate_public_host
* image_converter.convert_webp

### Dependency Changes

State exact dependency file that needs Pillow.

State whether FFmpeg is already available or only expected.

### API Additions

Propose a backward-compatible source inspection endpoint.

Propose optional fields:

* convert_webp
* webp_target

Do not remove or rename current fields.

### Security Findings

Report SSRF, redirect, size-limit, filename and directory risks.

### Exact Files To Modify

List exact paths.

### Exact Test Commands

Windows PowerShell only.

### Implementation Order

Give one milestone at a time.

Stop after the audit.

