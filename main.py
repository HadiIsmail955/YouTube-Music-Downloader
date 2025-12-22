import sys
import time
from pathlib import Path

from ytmusic_downloader.artist import (
    get_artist,
    get_albums,
    get_singles,
    get_playlists,
    get_songs,
)
from ytmusic_downloader.cli import print_menu, pick_items
from ytmusic_downloader.downloader import download
from ytmusic_downloader.utils import check_yt_dlp, build_music_url
from ytmusic_downloader.logger import setup_logger
from ytmusic_downloader.config import load_config


def folder_size(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def human_size(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return "∞"


def human_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <artist_id_or_url>")
        return

    logger = setup_logger()
    cfg = load_config()

    logger.info("Starting YouTube Music Downloader")
    logger.info(f"Active profile: {cfg.get('profile', 'normal')}")

    check_yt_dlp()

    artist_id = sys.argv[1]
    artist = get_artist(artist_id)
    artist_name = artist["name"]

    albums = get_albums(artist)
    singles = get_singles(artist)
    playlists = get_playlists(artist)
    songs = get_songs(artist)

    music_dir = Path(cfg["download_dir"])
    size_before = folder_size(music_dir)

    total_urls = 0
    start_time = time.time()

    while True:
        print_menu()
        choice = input("Choose [1-10]: ").strip()

        urls = []

        if choice == "1":
            urls = [build_music_url(a, "album") for a in albums]

        elif choice == "2":
            urls = [build_music_url(s, "single") for s in singles]

        elif choice == "3":
            urls = (
                [build_music_url(a, "album") for a in albums] +
                [build_music_url(s, "single") for s in singles]
            )

        elif choice == "4":
            urls = (
                [build_music_url(a, "album") for a in albums] +
                [build_music_url(s, "single") for s in singles] +
                [build_music_url(p, "playlist") for p in playlists]
            )

        elif choice == "5":
            selected = pick_items(albums, "albums")
            urls = [build_music_url(a, "album") for a in selected]

        elif choice == "6":
            selected = pick_items(playlists, "playlists")
            urls = [build_music_url(p, "playlist") for p in selected]

        elif choice == "7":
            selected = pick_items(songs, "songs")
            urls = [build_music_url(s, "song") for s in selected]

        elif choice == "8":
            urls = [input("Paste URL: ").strip()]

        elif choice == "9":
            break

        elif choice == "10":
            urls = (
                [build_music_url(a, "album") for a in albums] +
                [build_music_url(s, "single") for s in singles] +
                [build_music_url(p, "playlist") for p in playlists]
            )

        else:
            print("Invalid choice.")
            continue

        total_urls += len(urls)

        for url in urls:
            download(url, artist_name)

    elapsed = time.time() - start_time
    size_after = folder_size(music_dir)

    print("\n====== DOWNLOAD SUMMARY ======")
    print(f"Total URLs processed : {total_urls}")
    print(f"Total time           : {human_time(elapsed)}")
    print(f"Disk before          : {human_size(size_before)}")
    print(f"Disk after           : {human_size(size_after)}")
    print(f"Added                : {human_size(size_after - size_before)}")
    print("================================")

    logger.info("Session finished")


if __name__ == "__main__":
    main()

