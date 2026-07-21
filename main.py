import os
import re
from typing import Optional
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp

app = FastAPI(
    title="EXTREME Video Downloader",
    description="High-performance media downloader supporting custom formats, resolutions, and output paths.",
    version="2.0.0"
)

DEFAULT_DOWNLOAD_DIR = os.path.abspath("downloads")
os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EXTREME VIDEO DOWNLOADER</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4 font-sans">
        <div class="max-w-xl w-full bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 md:p-8">
            <div class="flex items-center space-x-3 mb-6">
                <div class="p-3 bg-red-600/20 text-red-500 rounded-xl">
                    <i class="fa-solid fa-bolt text-2xl text-red-500"></i>
                </div>
                <div>
                    <h1 class="text-2xl font-black tracking-wider text-white">EXTREME <span class="text-red-500">DOWNLOADER</span></h1>
                    <p class="text-xs text-slate-400">FastAPI & yt-dlp Core Engine</p>
                </div>
            </div>

            <form action="/download" method="post" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Target Media URL</label>
                    <input type="url" name="url" placeholder="https://www.youtube.com/watch?v=..." required 
                           class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-red-500 text-sm transition">
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">File Format</label>
                        <select name="file_type" id="file_type" onchange="updateQualityOptions()"
                                class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-red-500 text-sm">
                            <option value="mp4" selected>MP4 (Video)</option>
                            <option value="mkv">MKV (Video)</option>
                            <option value="webm">WEBM (Video)</option>
                            <option value="mp3">MP3 (Audio Only)</option>
                            <option value="m4a">M4A (Audio Only)</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Target Quality</label>
                        <select name="quality" id="quality" 
                                class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-red-500 text-sm">
                            <!-- Populated dynamically via JS -->
                        </select>
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Custom Download Directory (Optional)</label>
                    <input type="text" name="custom_dir" placeholder="E:\\Downloads or leave blank for default" 
                           class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-red-500 text-sm text-slate-300">
                </div>

                <button type="submit" 
                        class="w-full py-3.5 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl transition duration-200 shadow-lg shadow-red-600/20 flex items-center justify-center space-x-2">
                    <i class="fa-solid fa-download"></i>
                    <span>EXECUTE DOWNLOAD</span>
                </button>
            </form>
        </div>

        <script>
            function updateQualityOptions() {
                const fileType = document.getElementById('file_type').value;
                const qualitySelect = document.getElementById('quality');
                qualitySelect.innerHTML = '';

                if (['mp3', 'm4a'].includes(fileType)) {
                    const options = [
                        { val: '320', label: '320 kbps (Extreme Quality)' },
                        { val: '256', label: '256 kbps (High Quality)' },
                        { val: '192', label: '192 kbps (Medium Quality)' },
                        { val: '128', label: '128 kbps (Standard)' }
                    ];
                    options.forEach(opt => {
                        qualitySelect.innerHTML += `<option value="${opt.val}">${opt.label}</option>`;
                    });
                } else {
                    const options = [
                        { val: 'best', label: 'Best Available' },
                        { val: '2160p', label: '4K (2160p)' },
                        { val: '1080p', label: 'Full HD (1080p)' },
                        { val: '720p', label: 'HD (720p)' },
                        { val: '480p', label: 'SD (480p)' }
                    ];
                    options.forEach(opt => {
                        qualitySelect.innerHTML += `<option value="${opt.val}">${opt.label}</option>`;
                    });
                }
            }
            // Initialize options on page load
            updateQualityOptions();
        </script>
    </body>
    </html>
    """

@app.post("/download")
def download_media(
    url: str = Form(...),
    file_type: str = Form(...),
    quality: str = Form(...),
    custom_dir: Optional[str] = Form(None)
):
    # Determine target directory
    target_dir = DEFAULT_DOWNLOAD_DIR
    if custom_dir and custom_dir.strip():
        sanitized_path = os.path.abspath(custom_dir.strip())
        os.makedirs(sanitized_path, exist_ok=True)
        target_dir = sanitized_path

    outtmpl = os.path.join(target_dir, '%(title)s.%(ext)s')

    # Configure yt-dlp options based on audio vs video requests
    if file_type in ['mp3', 'm4a']:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': file_type,
                'preferredquality': quality,
            }],
            'quiet': True,
            'no_warnings': True,
        }
    else:
        # Construct height filter for video resolutions
        if quality != 'best' and quality.endswith('p'):
            height = quality.replace('p', '')
            format_str = f'bestvideo[height<={height}][ext={file_type}]+bestaudio/best[height<={height}]/best'
        else:
            format_str = f'bestvideo+bestaudio/best'

        ydl_opts = {
            'format': format_str,
            'merge_output_format': file_type,
            'outtmpl': outtmpl,
            'quiet': True,
            'no_warnings': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Handle post-processed extensions (e.g., converted to .mp3)
            if file_type in ['mp3', 'm4a']:
                base, _ = os.path.splitext(filename)
                filename = f"{base}.{file_type}"

        if not os.path.exists(filename):
            raise HTTPException(status_code=500, detail="File post-processing failed or file not found.")

        return FileResponse(
            filename,
            media_type="application/octet-stream",
            filename=os.path.basename(filename)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download execution error: {str(e)}")

