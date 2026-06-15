# How to run (make a new video)

Simple steps to make a video and post it yourself to YouTube / Instagram. You bring the **narration audio**
(make it on whatever website/tool you like); this project does the rest. Uploading is manual.

## 1. Prepare your two files in `uploads/`

- **`uploads/story.txt`** — put your **title on the first line** (it shows on the opening card and becomes
  the output filename). Anything below the first line is ignored.
- **`uploads/audio.mp3`** — your **narration**, named exactly `audio.mp3`. This is the voice you'll hear in
  the video. Replace it with a new file each time you make a video.

Keep it short — ~30–60 seconds of audio ≈ a normal Short/Reel.

## 2. Generate the video

```powershell
venvDigger\Scripts\python.exe make_video_from_text.py
```

- The finished video appears in the **`results\`** folder, named after your title.
- Length, background slice, etc. are all driven by your `audio.mp3`.

## 3. Add the captions

```powershell
venvDigger\Scripts\python.exe captionGen.py "results\<your title>.mp4"
```

Dont include the <>.
Also for easy copy paste, keep editing this :
venvDigger\Scripts\python.exe captionGen.py "results\Am I the asshole for accidentally getting my teacher banned from the school talent show.mp4"

This creates **`<your title>_out.mp4`** in the same folder. That `_out.mp4` is the final video.
(Vosk listens to your narration and times the on-screen words automatically; the small model
auto-downloads on first use.)

## 4. Post it (manually)

The `_out.mp4` is a normal 1080×1920 vertical video — the same file works for both:

- **YouTube**: youtube.com/upload (or YouTube Studio) → upload → mark it a Short.
- **Instagram**: upload the `_out.mp4` as a Reel.

---

## Customizing your videos

Most settings live in **`config.toml`** under `[settings]` / `[settings.background]`.
Edit that file and re-run. Here are the things you'll most likely want to change.

### Opening title card (the photo at the start)

This card is auto-generated every render. Things you can change:

- **The name on it**: `config.toml` →
  ```toml
  [settings]
  channel_name = "Your Channel Name"
  ```
- **How long it shows:** `title_card_seconds = 4` (seconds at the start of the video).
- **Turn it on/off:** `show_Reddit_Title = true` (set `false` to skip the intro card).
- **The card design itself:** it's drawn on top of **`assets\title_template.png`**. Replace that PNG with
  your own Reddit-post-style template to change the whole look.

### Background video & music

- **Background gameplay:** `config.toml` →
  ```toml
  [settings.background]
  background_video = "minecraft"
  ```
  Built-in options: `minecraft`, `minecraft-2`, `gta`, `motor-gta`, `rocket-league`, `csgo-surf`,
  `cluster-truck`, `multiversus`, `fall-guys`, `steep`. (Full list / add your own in
  **`utils\background_videos.json`**.) The first time you use a background it downloads once and caches.
  If you leave it blank, its random.
- **Background music:** `background_audio` — options `lofi`, `lofi-2`, `chill-summer` (list in
  `utils\background_audios.json`).
  If you leave it blank, its random.
- **Music volume / off:** `background_audio_volume = 0.15` (set to `0` for no music).

### Video size

- `resolution_w` / `resolution_h` — video size (default 1080×1920, the right size for Shorts/Reels).

---

Repeat from step 1 for the next video (new `audio.mp3`, new title). For _what's happening behind the
scenes_, see **[how it works.md](how%20it%20works.md)**.
