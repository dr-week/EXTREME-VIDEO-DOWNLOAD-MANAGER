---
# Source Intelligence and Media Conversion State

## Feature Goal

Recognize the submitted source, report realistic support capability,
download through the correct path, and convert WebP files when needed.

## Recognized Sources

* [ ] YouTube
* [ ] Instagram
* [ ] Pinterest
* [ ] TikTok
* [ ] Facebook
* [ ] X / Twitter
* [ ] Vimeo
* [ ] Dailymotion
* [ ] Reddit
* [ ] SoundCloud
* [ ] Twitch
* [ ] direct media
* [ ] generic websites

## Capability Model

* [ ] direct_download
* [ ] yt_dlp_known_extractor
* [ ] yt_dlp_probe_required
* [ ] generic_probe_required

## Backend

* [x] Source-recognition primitive added
* [x] Source-recognition tests added
* [ ] Existing API structure audited
* [ ] Source-inspection endpoint integrated
* [ ] Download request extended backward-compatibly
* [ ] Source metadata added to task status
* [ ] Probe errors normalized
* [ ] URL safety verified before network access

## Worker

* [x] WebP converter primitive added
* [x] WebP converter tests added
* [ ] Pillow added to worker dependency manifest
* [ ] WebP support verified
* [ ] Converter integrated after successful download
* [ ] Final yt-dlp path reliably captured
* [ ] Conversion result added to Celery result
* [ ] Original preservation verified
* [ ] Output-directory confinement verified

## Frontend

* [ ] Domain badge
* [ ] Source display name
* [ ] Content type
* [ ] Capability message
* [ ] Authentication warning
* [ ] Probe state
* [ ] WebP conversion selector
* [ ] Conversion result
* [ ] Reduced-motion transitions
* [ ] Mobile verification

## Security

* [ ] localhost blocked
* [ ] private IP blocked
* [ ] link-local blocked
* [ ] metadata endpoints blocked
* [ ] redirects reviewed
* [ ] maximum direct download size configured
* [ ] network timeout configured
* [ ] output paths confined
* [ ] cookie policy documented
* [ ] worker egress restrictions documented

## Current Approved Milestone

Audit the current backend router, request model, worker task and frontend
download flow before integrating the new primitives.

