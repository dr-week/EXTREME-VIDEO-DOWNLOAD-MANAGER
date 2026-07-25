---
name: ytdown-source-intelligence
description: Adds safe URL normalization, domain recognition, platform capability reporting, yt-dlp probing, direct media detection and source-aware UI behaviour to YTDOWN.
---

# YTDOWN Source Intelligence Skill

## Purpose

Recognize the source before starting a download.

Recognition is not the same as confirmed support.

Required flow:

URL entered
-> normalize URL
-> reject unsafe destinations
-> recognize platform
-> detect direct media
-> report probable capability
-> perform real extraction probe
-> dispatch download only after validation

## Required Reading

Before implementing this feature, read:

1. `.blackbox\PROJECT_STATE.md`
2. `.blackbox\FEATURE_SOURCE_MEDIA_STATE.md`
3. `.blackbox\WORKFLOW.md`
4. `.blackbox\skills\ytdown-core\SKILL.md`
5. `.blackbox\skills\ytdown-source-intelligence\SKILL.md`
6. backend request models
7. backend routers
8. backend Celery dispatch code
9. worker yt-dlp task
10. frontend request and polling code
11. relevant tests
12. current Git diff

## Recognition Registry

Recognize at minimum:

- YouTube
- Instagram
- Pinterest
- TikTok
- Facebook
- X / Twitter
- Vimeo
- Dailymotion
- Reddit
- SoundCloud
- Twitch
- direct image URLs
- direct video URLs
- direct audio URLs
- generic websites

## Capability Levels

Use exactly these meanings:

### direct_download

The URL path identifies a direct media file.

The downloader must still validate:

- final HTTP status
- content length
- content type
- redirects
- maximum size
- public destination address

### yt_dlp_known_extractor

The platform is associated with a known yt-dlp extractor.

This does not guarantee that the exact URL works.

A metadata probe is still required.

### yt_dlp_probe_required

The platform is recognized, but dedicated or reliable support is not guaranteed.

Pinterest belongs in this category.

### generic_probe_required

The domain is not in the local recognition registry.

Try the yt-dlp generic extractor without claiming support first.

## Platform Rules

### YouTube

Recognize:

- youtube.com
- youtu.be
- youtube-nocookie.com
- Shorts
- normal videos
- playlists

Do not bypass:

- DRM
- paid access
- private content
- age or account restrictions

### Instagram

Recognize:

- posts
- reels
- stories
- profile URLs

Display that authentication may be required.

Do not automatically import browser cookies.

Cookie use requires explicit user configuration and secure storage.

### Pinterest

Recognize:

- pinterest.com
- pin.it
- approved regional Pinterest domains
- pin URLs

Do not claim that Pinterest is always supported.

Do not create a fragile HTML scraper merely because yt-dlp probing fails.

Return a clear unsupported, authentication-required or probe-failed status.

## Direct Media Rules

Detect common extensions:

Images:

- jpg
- jpeg
- png
- gif
- webp
- avif
- heic
- bmp
- tif
- tiff

Video:

- mp4
- webm
- mov
- mkv
- m4v
- avi
- mpeg
- mpg

Audio:

- mp3
- m4a
- wav
- flac
- aac
- ogg
- opus
- wma

Do not trust the filename extension alone.

The worker must verify the actual response Content-Type and downloaded file.

## URL Safety

Reject:

- localhost
- loopback IP addresses
- private IP addresses
- link-local addresses
- cloud metadata addresses
- internal hostnames
- URL credentials
- unsupported schemes
- nonstandard ports unless explicitly approved

Resolve the hostname immediately before network access.

Application validation is not sufficient by itself.

Production networking must prevent worker access to:

- instance metadata
- private subnets not required by the service
- internal administration services

## API Design

Add a source inspection operation through the existing API router style.

Do not invent a new application root.

The response should include:

- normalized_url
- hostname
- platform
- display_name
- input_type
- content_kind
- capability
- requires_probe
- authentication_may_be_required
- detected_extension
- webp_conversion_available
- note

## Download Request Compatibility

Any new request fields must be optional with backward-compatible defaults.

Recommended fields:

- convert_webp: true
- webp_target: auto

Allowed webp_target values:

- auto
- png
- jpeg
- gif

Existing clients without these fields must continue working.

## Probe Rules

A probe must:

- use the installed yt-dlp Python API
- set download to false
- use a finite socket timeout
- avoid unrestricted playlists during inspection
- return structured metadata
- sanitize errors
- avoid exposing cookies or tokens
- never report success when extraction failed

## User Rights

The product must remind users to download only media they own or are authorized to save.

Do not add DRM circumvention, paywall bypass or private-content bypass functionality.

## Tests

Add tests for:

- YouTube video
- YouTube Short
- Instagram Reel
- Pinterest pin
- direct WebP URL
- generic URL
- missing scheme
- invalid scheme
- private IP rejection
- localhost rejection
- nonstandard port rejection
- fragmented URL normalization

## Stop Rule

Source recognition and actual source probing are separate milestones.

Do not redesign the UI during backend source implementation.

Do not begin WebP conversion integration until recognition tests pass.

