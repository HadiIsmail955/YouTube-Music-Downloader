import shutil
import sys


def check_yt_dlp():
    if not shutil.which("yt-dlp"):
        print("ERROR: yt-dlp is not installed or not in PATH.")
        print("Install it first: https://github.com/yt-dlp/yt-dlp")
        sys.exit(1)

def build_music_url(item, item_type):
    if item_type in ("album", "single"):
        return f"https://music.youtube.com/browse/{item['browseId']}"

    if item_type == "playlist":
        return f"https://music.youtube.com/playlist?list={item['browseId']}"

    if item_type == "song":
        return f"https://music.youtube.com/watch?v={item['videoId']}"

    raise ValueError("Unknown item type")
