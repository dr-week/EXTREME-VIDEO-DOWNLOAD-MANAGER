# EXTREME VIDEO DOWNLOADER

A high-performance, engineering-grade web tool designed to extract and convert online media. Built with **FastAPI** and **yt-dlp**, featuring customizable formats, resolutions, bitrates, and targeted local directories.

---

## Features

- **Format Selection:** Video (`MP4`, `MKV`, `WEBM`) and Audio (`MP3`, `M4A`).
- **Quality Control:** Up to 4K (`2160p`, `1080p`, `720p`, `480p`) or high bitrates (`320kbps`, `256kbps`, `192kbps`).
- **Custom Destination Path:** Save files directly to system paths (e.g., `D:\Media` or local subfolders).
- **FastAPI Core:** Asynchronous request handler for high throughput.

---

## Prerequisites

1. **Python 3.10+**
2. **FFmpeg installed on System Path** *(Required for audio extraction & video merging)*
   - **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or run `winget install ffmpeg`.

---

## Local Setup

1. **Clone Repository:**
   ```bash
   git clone https://github.com/dr-week/EXTREME-VIDEO-DOWNLOAD-MANAGER.git
   cd EXTREME-VIDEO-DOWNLOAD-MANAGER
   ```

2. **Set Up Virtual Environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run Application:**
   ```powershell
   uvicorn main:app --reload
   ```

5. **Access Interface:** Open `http://127.0.0.1:8000` in your browser.

