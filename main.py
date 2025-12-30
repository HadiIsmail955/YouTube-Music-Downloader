import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from ytmusic_downloader.artist import (
    get_artist,
    get_albums,
    get_singles,
    get_playlists,
)
from ytmusic_downloader.downloader import download
from ytmusic_downloader.logger import setup_logger
from ytmusic_downloader.config import load_config
from ytmusic_downloader.utils import (
    check_yt_dlp,
    build_music_url,
    resolve_artist_from_url,
)

def is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def folder_size(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def human_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"


def human_size(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return "∞"

def parallel_download(jobs, workers):
    completed = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(download, url, artist) for url, artist in jobs]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Download failed: {e}")
            completed += 1

    return completed

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <artist | url | file.txt>")
        return

    logger = setup_logger()
    cfg = load_config()
    check_yt_dlp()

    arg = sys.argv[1]
    music_dir = Path(cfg["download_dir"])
    workers = int(cfg.get("parallel_downloads", 4))
    auto_update = bool(cfg.get("auto_update", True))

    size_before = folder_size(music_dir)
    start_time = time.time()
    jobs = []

    if Path(arg).exists() and arg.endswith(".txt"):
        lines = [
            line.strip()
            for line in Path(arg).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]

        print("\n==============================")
        print("MIXED FILE MODE (AUTO-UPDATE)")
        print("==============================")
        print(f"Entries: {len(lines)}")
        print(f"Parallel workers: {workers}\n")

        for entry in lines:

            # -------------------------------
            # URL ENTRY
            # -------------------------------
            if is_url(entry):
                artist_name = resolve_artist_from_url(entry) or "Unknown Artist"
                jobs.append((entry, artist_name))

            # -------------------------------
            # ARTIST ENTRY (AUTO-UPDATE)
            # -------------------------------
            else:
                try:
                    artist = get_artist(entry)
                    artist_name = artist["name"]

                    print(f"Checking artist: {artist_name}")

                    albums = get_albums(artist)
                    singles = get_singles(artist)
                    playlists = get_playlists(artist)

                    urls = (
                        [build_music_url(a, "album") for a in albums] +
                        [build_music_url(s, "single") for s in singles] +
                        [build_music_url(p, "playlist") for p in playlists]
                    )

                    for url in urls:
                        jobs.append((url, artist_name))

                except Exception as e:
                    print(f"Failed artist {entry}: {e}")

    elif is_url(arg):
        artist_name = resolve_artist_from_url(arg) or "Unknown Artist"
        jobs.append((arg, artist_name))

    else:
        artist = get_artist(arg)
        artist_name = artist["name"]

        print(f"\n Artist: {artist_name}")

        albums = get_albums(artist)
        singles = get_singles(artist)
        playlists = get_playlists(artist)

        urls = (
            [build_music_url(a, "album") for a in albums] +
            [build_music_url(s, "single") for s in singles] +
            [build_music_url(p, "playlist") for p in playlists]
        )

        for url in urls:
            jobs.append((url, artist_name))

    print(f"\nStarting downloads: {len(jobs)} jobs\n")
    completed = parallel_download(jobs, workers)

    elapsed = time.time() - start_time
    size_after = folder_size(music_dir)

    print("\n====== DOWNLOAD SUMMARY ======")
    print(f"Jobs processed       : {completed}")
    print(f"Total time           : {human_time(elapsed)}")
    print(f"Disk before          : {human_size(size_before)}")
    print(f"Disk after           : {human_size(size_after)}")
    print(f"Added                : {human_size(size_after - size_before)}")
    print("================================")

    logger.info("Session finished")


if __name__ == "__main__":
    main()
