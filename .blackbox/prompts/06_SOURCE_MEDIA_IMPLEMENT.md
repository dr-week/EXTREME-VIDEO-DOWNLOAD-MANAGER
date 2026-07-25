Use these skills:

* ytdown-core
* ytdown-source-intelligence
* ytdown-media-conversion

Read the completed source-media audit first.

Implement backend and worker source-media support only.

Do not redesign the frontend in this milestone.

Required results:

1. Integrate source recognition into the existing backend structure.
2. Add a backward-compatible source inspection endpoint.
3. Preserve the existing download endpoint.
4. Preserve all existing required request fields.
5. Add optional fields only when compatible:

   * convert_webp, default true
   * webp_target, default auto
6. Pass source and conversion options safely to the Celery task.
7. Resolve and validate the public hostname immediately before downloading.
8. Continue using yt-dlp for supported and generic media pages.
9. Treat Pinterest as recognized but probe-required.
10. Do not promise Pinterest support before a probe succeeds.
11. Do not add custom Pinterest HTML scraping.
12. Add Pillow to the correct worker dependency manifest.
13. Integrate convert_webp only after a successful download.
14. Verify the real downloaded file is WebP.
15. Preserve the original WebP by default.
16. Return conversion metadata through the existing task result.
17. Do not change existing task-state meanings.
18. Sanitize errors sent to the frontend.
19. Do not expose cookies, tokens, filesystem secrets or stack traces.
20. Add tests for all changed behaviour.

Security requirements:

* reject localhost
* reject private IPs
* reject link-local addresses
* reject metadata endpoints
* reject URL credentials
* reject unsupported schemes
* use timeouts
* limit direct media response size
* confine output paths to the approved output directory
* validate redirects where the current HTTP client allows it
* do not bypass DRM
* do not bypass paid or private content

Validation:

Run actual backend tests.

Run actual worker tests.

Verify Pillow:

```powershell
Set-Location "E:\CODES\001\YTDOWN\worker"

python -c "from PIL import features; print(features.check_module('webp'))"
```

Then:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

git diff --check
git status
```

Use Windows PowerShell commands only.

Stop after backend and worker validation.

Do not modify the frontend.
Do not begin Docker Compose.
Do not deploy.
Do not merge.
Do not push.

