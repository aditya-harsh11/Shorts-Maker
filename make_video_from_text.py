#!/usr/bin/env python
"""
Build a video from a title + your own narration audio file.

Usage:
    python make_video_from_text.py

It reads two things from the `uploads/` folder:
    - uploads/story.txt   : first non-empty line = the title (shown on the
                            title card + used for the output filename). Anything
                            below it is ignored (kept only for your reference).
    - uploads/audio.mp3   : the narration you generated yourself. This IS the
                            voice track of the video — drop a new one in each run.

The pipeline lays your audio over random muted gameplay, shows the Reddit-style
title card for the first few seconds, and renders results/<title>.mp4. Add the
on-screen captions afterwards with:  python captionGen.py "results/<title>.mp4"
"""
import argparse
import math
import sys
import time
from pathlib import Path

# Windows consoles default to cp1252, which crashes when rich/print emit emojis.
# Force UTF-8 so it never dies on an encoding error, regardless of how launched.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import ffmpeg

from utils import settings
from utils.console import print_step, print_substep
from utils.ffmpeg_install import ffmpeg_install
from utils.id import id
from video_creation.background import (
    chop_background,
    download_background_audio,
    download_background_video,
    get_background_config,
)
from video_creation.final_video import make_final_video

UPLOADS = Path("uploads")
STORY_FILE = UPLOADS / "story.txt"
AUDIO_FILE = UPLOADS / "audio.mp3"


def read_title(path: Path) -> str:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        print_substep(f"'{path}' is empty. Put your title on the first line.", style="red")
        sys.exit(1)
    title = raw.splitlines()[0].strip()
    if not title:
        print_substep("Your story file needs a title on the first line.", style="red")
        sys.exit(1)
    return title


def build_reddit_object(title: str) -> dict:
    """Minimal object the render pipeline expects: a title (for the card +
    filename) and a unique id (used for the temp folder + ledger)."""
    return {
        "thread_title": title,
        "thread_id": str(int(time.time())),  # unique per run
    }


def main():
    title = read_title(STORY_FILE)
    print_step(f"Building video for: {title}")

    reddit_object = build_reddit_object(title)
    redditid = id(reddit_object)

    # Length comes straight from your narration audio.
    length = math.ceil(float(ffmpeg.probe(str(AUDIO_FILE))["format"]["duration"]))

    bg_config = {
        "video": get_background_config("video"),
        "audio": get_background_config("audio"),
    }
    download_background_video(bg_config["video"])
    download_background_audio(bg_config["audio"])

    # chop_background writes into assets/temp/<id>/, make sure it exists first.
    Path(f"assets/temp/{redditid}").mkdir(parents=True, exist_ok=True)
    chop_background(bg_config, length, reddit_object)

    make_final_video(length, reddit_object, bg_config, str(AUDIO_FILE))


if __name__ == "__main__":
    if sys.version_info.major != 3 or sys.version_info.minor not in [10, 11, 12]:
        print("This program requires Python 3.10, 3.11, or 3.12.")
        sys.exit()

    parser = argparse.ArgumentParser(
        description="Render a short video from uploads/story.txt (title) + uploads/audio.mp3 (narration)."
    )
    parser.parse_args()

    if not STORY_FILE.exists():
        print(f"Missing {STORY_FILE}. Put your title on line 1 of that file.")
        sys.exit(1)
    if not AUDIO_FILE.exists():
        print(f"Missing {AUDIO_FILE}. Drop your narration mp3 there (named audio.mp3) and re-run.")
        sys.exit(1)

    ffmpeg_install()
    directory = Path().absolute()
    config = settings.check_toml(
        f"{directory}/utils/.config.template.toml", f"{directory}/config.toml"
    )
    if config is False:
        sys.exit()

    main()
