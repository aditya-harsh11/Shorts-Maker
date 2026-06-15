# Story Video Generator

Turn a title + your own narration audio into a captioned, vertical (1080×1920) short video —
your voice track over muted gameplay footage with CapCut-style one-word captions. You then upload it
**manually** to YouTube Shorts and/or Instagram Reels.

## Make a video

See **[notes/how to run.md](notes/how%20to%20run.md)** for the full steps (and
**[notes/how it works.md](notes/how%20it%20works.md)** for what happens under the hood). Short version:

```powershell
# 1. Put your title on line 1 of  uploads\story.txt
# 2. Put your narration in        uploads\audio.mp3
# 3. Generate:
venvDigger\Scripts\python.exe make_video_from_text.py
# 4. Caption:
venvDigger\Scripts\python.exe captionGen.py "results\<your title>.mp4"
# 5. Upload the _out.mp4 to YouTube / Instagram yourself.
```

## First-time setup

```bash
python -m venv venvDigger
venvDigger\Scripts\python.exe -m pip install -r requirements.txt
```

You also need `ffmpeg` on PATH (any modern build). The first render auto-downloads the background video
via `yt-dlp` (cached afterward); `captionGen.py` auto-downloads a small Vosk speech model on first use.

## Config

Settings live in `config.toml` (gitignored). Useful knobs: `channel_name` (the opening-card name),
`title_card_seconds`, `background_video`, `background_audio`, `resolution_w`/`resolution_h`.
