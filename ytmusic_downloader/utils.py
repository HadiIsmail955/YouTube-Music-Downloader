import shutil
import sys
from pathlib import Path
from ytmusicapi import YTMusic
from urllib.parse import urlparse, parse_qs

ytmusic = YTMusic()

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

def resolve_artist_from_url(url: str) -> str:
    parsed = urlparse(url)

    if "watch" in parsed.path:
        video_id = parse_qs(parsed.query).get("v", [None])[0]
        if video_id:
            song = ytmusic.get_song(video_id)
            artists = song.get("videoDetails", {}).get("author")
            if artists:
                return artists

    if "playlist" in parsed.path:
        playlist_id = parse_qs(parsed.query).get("list", [None])[0]
        if playlist_id:
            pl = ytmusic.get_playlist(playlist_id, limit=1)
            if pl.get("author"):
                return pl["author"]["name"]

    if "browse" in parsed.path:
        browse_id = parsed.path.split("/")[-1]
        album = ytmusic.get_album(browse_id)
        if album.get("artists"):
            return album["artists"][0]["name"]

    return "Unknown Artist"

def parse_urls(arg: str):
    p = Path(arg)

    if p.exists() and p.is_file():
        return [
            line.strip()
            for line in p.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    if "," in arg or "\n" in arg:
        return [u.strip() for u in arg.replace("\n", ",").split(",") if u.strip()]

    return [arg]