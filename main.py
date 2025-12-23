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
from ytmusic_downloader.logger import setup_logger
from ytmusic_downloader.config import load_config
from ytmusic_downloader.utils import (
    check_yt_dlp,
    build_music_url,
    resolve_artist_from_url,
    parse_urls,
)


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
        print("Usage:")
        print("  python main.py <artist_id>")
        print("  python main.py <url>")
        print("  python main.py urls.txt")
        return

    logger = setup_logger()
    cfg = load_config()
    check_yt_dlp()

    arg = sys.argv[1]

    music_dir = Path(cfg["download_dir"])
    size_before = folder_size(music_dir)
    start_time = time.time()
    total_urls = 0

    if arg.startswith("http") or Path(arg).exists():
        urls = parse_urls(arg)

        print("\n==============================")
        print("URL DOWNLOAD MODE")
        print("==============================")
        print(f"Total URLs: {len(urls)}\n")

        for url in urls:
            artist_name = resolve_artist_from_url(url)

            if not artist_name or artist_name.strip() == "":
                artist_name = "Unknown Artist"

            download(url, artist_name)
            total_urls += 1

    else:
        artist = get_artist(arg)
        artist_name = artist["name"]

        albums = get_albums(artist)
        singles = get_singles(artist)
        playlists = get_playlists(artist)
        songs = get_songs(artist)

        print("\n==============================")
        print("ARTIST MODE")
        print("==============================")
        print(f"Artist: {artist_name}\n")

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
                urls = parse_urls(input("Paste URL(s): ").strip())

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

            for url in urls:
                download(url, artist_name)
                total_urls += 1

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
