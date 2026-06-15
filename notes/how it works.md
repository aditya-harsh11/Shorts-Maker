# How it works

Plain-English walkthrough of what happens from your files to a finished video. Two commands do it all:
`make_video_from_text.py` builds the video, `captionGen.py` adds the captions.

## The big picture
You give it a **title** + your **own narration audio**, it gives back a **captioned vertical video**.
There is **no built-in text-to-speech** — you make the voice clip yourself (any tool/website you like) and
drop it in. The only "intelligence" left is speech-to-text for caption timing. Everything else is just
image/video assembly with ffmpeg.

---

## Step 1 — You provide two files (in `uploads/`)
- **`uploads/story.txt`** — the **first line is the title** (shown on the opening card and used for the
  output filename). Anything below the first line is ignored (keep notes there if you like).
- **`uploads/audio.mp3`** — your **narration**. This IS the voice track of the video. Replace it each run.

## Step 2 — Measure the narration
`make_video_from_text.py` reads how long `audio.mp3` is. That length drives everything else (how much
gameplay to cut, how long the video is).

## Step 3 — The background footage
It grabs a **gameplay video** (Minecraft by default), downloaded once via `yt-dlp` and cached. Then it:
- crops it to vertical (1080×1920),
- cuts a **random slice** exactly as long as your narration,
- mutes it and optionally mixes in quiet background music.

A different random chunk each time keeps videos from looking repetitive.

## Step 4 — The opening title card
The "Reddit Tales / your title" card is **auto-generated** each run: a blank Reddit-post template image
(`assets/title_template.png`) with your **channel name** and **title** drawn on it. It shows for the
**first few seconds** of the video (configurable via `title_card_seconds`).

## Step 5 — Stitch it together
`ffmpeg` combines: background clip + your narration audio (+ optional music) + the title card overlay.
Output: `results/<title>.mp4` — finished video, but **no on-screen words yet** (just the title card over
narrated gameplay).

## Step 6 — The captions
`captionGen.py` is the clever part:
- It **listens to the narration** with a speech-to-text model (Vosk) and finds exactly **when each word is
  spoken** (timestamps).
- For each word it renders a big white outlined image and overlays it **right when it's said** — the
  CapCut-style one-word captions.
- Saves `<title>_out.mp4`. That's your final video.

## Step 7 — You post it
Upload that `_out.mp4` to YouTube/Instagram yourself.

---

### Mental model
> Your title + your own audio → laid over random muted gameplay → title card on the front → rendered
> → then a speech recognizer re-listens and stamps the words on screen as captions.

### Which file does what
| Step | File |
|---|---|
| Entry point: reads title + audio, runs the pipeline | `make_video_from_text.py` |
| Background download + crop + random slice | `video_creation/background.py` |
| Title card + final ffmpeg render | `video_creation/final_video.py` |
| Captions (speech-to-text overlay) | `captionGen.py` (Vosk) |
