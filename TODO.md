# Phase 1 Tasks

- [x] Environment setup (venv, deps)
- [x] **1. Fix `prepare_filename` bug** — Use `%(id)s` template for deterministic path
- [x] **2. Improve UI with JS** — Fetch + spinner + status + auto-download
- [x] **3. Enhanced error handling** — User-friendly yt-dlp error messages
- [x] **4. Add `restrictfilenames`** — Safe filenames
- [x] **5. Launch & test** — `uvicorn main:app --reload`

---

# Phase 2 Tasks — EXTREME UPGRADE

- [x] **1. Create `requirements.txt`** — Dependencies: fastapi, uvicorn, yt-dlp, python-multipart, jinja2
- [x] **2. Create `.gitignore`** — Ignore venv, downloads, media files, IDE files
- [x] **3. Create `README.md`** — Full project documentation with setup instructions
- [x] **4. Rewrite `main.py`** — EXTREME Video Downloader with:
  - [x] FastAPI metadata (title, description, version 2.0.0)
  - [x] Dynamic format selection (MP4, MKV, WEBM, MP3, M4A)
  - [x] Dynamic quality options (resolution for video, bitrate for audio)
  - [x] Custom download directory input
  - [x] Tailwind CSS + Font Awesome UI
  - [x] Audio extraction via FFmpegExtractAudio post-processor
  - [x] Video format string with height filtering
- [x] **5. Initialize Git repo, stage, commit & push to GitHub**

