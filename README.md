# YouTube Music Downloader

A simple, professional CLI tool to download albums, singles, playlists,
or individual songs from YouTube Music directly to your laptop.

The tool is interactive, easy to use, and automatically skips music
that has already been downloaded.

---

## Features

- Download albums, singles, playlists, or songs
- Pick everything or select specific items
- Clean folder structure (Artist / Album / Song)
- Automatically skips already downloaded music
- Central configuration file
- No login, no accounts, no tracking
- Works on Windows, macOS, and Linux

Powered by:
- ytmusicapi
- yt-dlp

---

## Requirements

### 1️- Python 3.9 or newer
Check your version:
```bash
python --version
```

---

### 2- Install Python dependencies
```bash
pip install -r requirements.txt
```

---

## Project Structure

```text
ytmusic-downloader/
│
├── config/
│   └── config.yml
├── data/
│   └── download_archive.txt
├── Music/
├── ytmusic_downloader/
├── main.py
├── requirements.txt
├── README.md
├── HELPER.md
└── LICENSE
```

---

## How to Use

```bash
python main.py <artist_or_album_or_playlist_or_song_url>
```

---

## Updating / Checking for New Music

Just run the same command again. Already downloaded content is skipped automatically.

---

## Disclaimer

For personal use only. Please respect copyright laws.
