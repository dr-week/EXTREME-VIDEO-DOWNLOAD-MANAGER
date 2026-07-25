---
name: ytdown-media-conversion
description: Adds safe post-download WebP inspection and conversion to PNG, JPEG or GIF while preserving originals and preventing silent animation or transparency loss.
---

# YTDOWN Media Conversion Skill

## Purpose

Convert downloaded WebP media into a more useful output format.

Required flow:

download completes
-> determine actual file path
-> verify the file exists
-> inspect actual image format
-> detect animation
-> detect transparency
-> select safe output
-> write temporary output
-> atomically replace target
-> preserve original by default
-> return conversion metadata

## Required Reading

Before integration, read:

1. `.blackbox\FEATURE_SOURCE_MEDIA_STATE.md`
2. `.blackbox\skills\ytdown-core\SKILL.md`
3. `.blackbox\skills\ytdown-media-conversion\SKILL.md`
4. worker dependency file
5. worker Celery task
6. worker output filename logic
7. worker tests
8. backend task-status response
9. frontend result display
10. current Git diff

## Dependency

Use Pillow.

Before adding Pillow:

- inspect whether it already exists
- identify requirements.txt, pyproject.toml or another dependency source
- add it to the correct worker dependency file
- update the correct lock file when one exists

Do not rely only on a local pip installation.

## WebP Support Check

Check Pillow WebP support at runtime.

If unavailable:

- fail clearly
- do not create an empty output
- preserve the downloaded original
- return a structured conversion error

## Automatic Conversion

When target is `auto`:

- animated WebP -> GIF
- static WebP with transparency -> PNG
- static opaque WebP -> JPEG

This avoids silently removing animation or transparency.

## Explicit Conversion

Allowed targets:

- png
- jpeg
- gif

Animated WebP to PNG or JPEG must fail unless the product explicitly introduces a first-frame-only option later.

Do not silently discard frames.

## Original File Policy

Preserve the original WebP by default.

Deletion is allowed only through an explicit option after successful conversion.

Never delete the source before the converted output has been verified.

## Output Safety

The converter must:

- verify actual image format using Pillow
- reject fake .webp files
- avoid overwriting by default
- write to a temporary file
- atomically rename after success
- keep output within the approved download directory
- return size, dimensions and final path
- sanitize user-controlled filenames

## Worker Integration

Add optional download request fields:

- convert_webp: boolean, default true
- webp_target: auto, png, jpeg or gif

After download:

1. resolve the actual final yt-dlp file path
2. inspect the suffix and actual image format
3. convert only when it is WebP
4. preserve original unless configured otherwise
5. include conversion result in task status

Do not run WebP conversion on video WebM files.

WebP and WebM are different formats.

## Task Result

Recommended additional result fields:

- original_file
- final_file
- original_format
- final_format
- converted
- conversion_target
- conversion_error
- width
- height
- animated
- frame_count
- output_size_bytes

Keep existing result fields intact.

## Frontend Behaviour

Show conversion controls only when relevant.

Possible states:

- WebP detected
- converting
- converted to PNG
- converted to JPEG
- converted to GIF
- conversion failed; original retained

Do not display fake conversion progress.

## Tests

Test:

- opaque WebP to JPEG
- transparent WebP to PNG
- explicit PNG conversion
- overwrite protection
- explicit overwrite
- fake WebP rejection
- original preservation
- explicit source deletion
- output metadata
- Pillow WebP availability

## Validation

Run actual worker test commands.

Then verify Pillow support:

```powershell
python -c "from PIL import features; print(features.check_module('webp'))"
```

Use Windows PowerShell only.

## Stop Rule

Stop after worker conversion tests pass.

Do not change the frontend in the same milestone unless explicitly approved.

