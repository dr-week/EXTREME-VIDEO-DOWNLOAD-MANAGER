---
# YTDOWN Source Recognition and Media Conversion Plan

## Objective

Allow the application to recognize common source domains, report realistic
download capability, route downloads correctly, and convert downloaded WebP
files when appropriate.

## Feature Flow

User enters URL
-> backend normalizes URL
-> backend blocks unsafe destinations
-> backend identifies platform
-> frontend displays source badge
-> backend or worker performs yt-dlp probe
-> task is submitted
-> worker downloads media
-> worker determines actual final file
-> WebP is converted when enabled
-> final result is returned
-> frontend displays final format and path

## Recognition Is Not Support

A recognized domain means the product knows the platform name.

It does not guarantee that the exact URL can be downloaded.

Support must be confirmed through an actual probe.

## Capability Classes

### direct_download

For direct media URLs.

### yt_dlp_known_extractor

For known platforms such as YouTube and Instagram.

### yt_dlp_probe_required

For recognized platforms where reliable extractor support is not guaranteed.

Pinterest belongs here.

### generic_probe_required

For other websites handled through yt-dlp generic extraction.

## Milestone 1 — Audit

Inspect actual backend, worker and frontend contracts.

No changes.

## Milestone 2 — Backend Source Inspection

Integrate source_recognizer.py.

Add a source-inspection endpoint using the existing router structure.

Keep the existing download endpoint compatible.

## Milestone 3 — Worker Probe and Security

Add a safe yt-dlp metadata probe.

Validate hostname resolution before network access.

Add timeouts and direct-file size limits.

## Milestone 4 — WebP Integration

Add Pillow to the worker dependency manifest.

Integrate image_converter.py after downloads complete.

Keep original WebP by default.

## Milestone 5 — Task Result

Return:

* detected platform
* content type
* original file
* final file
* conversion status
* final format
* dimensions
* animation state
* size

## Milestone 6 — Frontend

Add:

* source badge
* source capability
* authentication warning
* WebP conversion selector
* conversion state
* final format
* restrained animations

## Milestone 7 — Security

Verify:

* SSRF protection
* private network blocking
* metadata endpoint blocking
* redirect behaviour
* maximum size
* output path confinement
* cookie storage policy
* worker egress rules

## Milestone 8 — Documentation and CI

Document supported capability categories.

Add source-recognition and image-conversion tests to CI.

Do not advertise every recognized site as guaranteed.

