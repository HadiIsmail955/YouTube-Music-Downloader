# YouTube Music Downloader

A simple, professional CLI tool to download **albums, singles, playlists, or individual songs**
from **YouTube Music** directly to your laptop.

The tool is interactive, easy to use, and automatically skips music
that has already been downloaded — making it ideal for long‑term music
library management and re‑syncing (including Apple Music).

---

## Features

- Download **albums, singles, playlists, or individual songs**
- Interactive menu for artist pages
- Support for **direct URLs** and **URL lists**
- Clean folder structure: `Artist / Album / Track`
- Automatically skips already downloaded music
- Apple Music–friendly metadata & structure
- Central configuration file
- No login, no accounts, no tracking
- Cross‑platform: **Windows, macOS, Linux**

Powered by:
- **ytmusicapi**
- **yt-dlp**
- **ffmpeg**
- **AtomicParsley**

---

## Requirements

### 1 - Python 3.9 or newer

Check your version:
```bash
python --version
```

---

### 2 - Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 3 -  Install yt-dlp (REQUIRED)

This tool **does not install yt-dlp automatically**.  
It must be installed **system‑wide** and available in your `PATH`.

The tool checks this at runtime using:

```python
def check_yt_dlp():
    if not shutil.which("yt-dlp"):
        print("ERROR: yt-dlp is not installed or not in PATH.")
        print("Install it first: https://github.com/yt-dlp/yt-dlp")
        sys.exit(1)
```

#### ▶ Windows
```powershell
pip install -U yt-dlp
```

Verify:
```powershell
yt-dlp --version
```

---

#### ▶ macOS (Homebrew recommended)
```bash
brew install yt-dlp
```

Verify:
```bash
yt-dlp --version
```

---

#### ▶ Linux
```bash
pip install -U yt-dlp
```

or (Debian / Ubuntu):
```bash
sudo apt install yt-dlp
```

Verify:
```bash
yt-dlp --version
```

---

### 4 - Install ffmpeg (REQUIRED)

`ffmpeg` is **mandatory** for audio extraction.
If it is missing, downloads will fail.

---

#### ▶ Windows

1. Download a static build from:
   https://www.gyan.dev/ffmpeg/builds/
2. Extract the archive
3. Add `ffmpeg/bin` to your **PATH**
4. Restart your terminal

Verify:
```powershell
ffmpeg -version
```

---

#### ▶ macOS
```bash
brew install ffmpeg
```

Verify:
```bash
ffmpeg -version
```

---

#### ▶ Linux
```bash
sudo apt install ffmpeg
```

Verify:
```bash
ffmpeg -version
```

---

## Project Structure

```text
ytmusic-downloader/
│
├── config/
│   └── config.yml              # User configuration (audio format, profiles, paths)
│
├── data/
│   └── download_archive.txt    # yt-dlp archive (prevents re-downloading)
│
├── Music/                      # Downloaded music output
│   └── Artist/
│       └── Album/
│           └── Track.mp3
│
├── ytmusic_downloader/         # Core application package
│   ├── __init__.py
│   ├── artist.py               # Artist & metadata handling (ytmusicapi)
│   ├── cli.py                  # Interactive menu & selections
│   ├── config.py               # Config loader & path normalization
│   ├── downloader.py           # yt-dlp execution (safe wrapper)
│   ├── logger.py               # Logging setup
│   └── utils.py                # Helpers (URL parsing, artist resolution, checks)
│
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
│
├── README.md                   # Main documentation & setup guide
├── CONTRIBUTING.md             # Contribution rules (no PRs, personal use only)
├── NOTICE                      # Third-party notices & legal disclaimers
├── LICENSE                     # Proprietary personal-use license
└── .gitignore                  # Git ignore rules (recommended)
```

---

## How to Use

### ▶ Download from an artist page
```bash
python main.py <artist_id>
```

You will be presented with an interactive menu:
- All albums
- Singles
- Playlists
- Specific selections

---

### ▶ Download a single song / album / playlist
```bash
python main.py https://music.youtube.com/watch?v=XXXX
python main.py https://music.youtube.com/playlist?list=XXXX
python main.py https://music.youtube.com/browse/XXXX
```

---

### ▶ Download a list of URLs

Create a file (for example `urls.txt`):

```text
https://music.youtube.com/watch?v=XXXX
https://music.youtube.com/playlist?list=YYYY
https://music.youtube.com/browse/ZZZZ
```

Then run:
```bash
python main.py urls.txt
```

---

## Updating / Checking for New Music

Just run the same command again.

Already downloaded tracks are automatically skipped using:
```
data/download_archive.txt
```

This makes the tool safe to run repeatedly.

---

## Configuration

All settings are stored in:
```
config/config.yml
```

You can control:
- Audio format
- Download directory
- Speed / performance profiles
- Retry behavior
- Rate limiting
- Metadata embedding

---

## License

This project is **NOT open source**.

It is provided for **personal use only**.
Commercial use, redistribution, and illegal use are strictly prohibited.
Please respect copyright laws and the terms of service of YouTube Music.

See the LICENSE file for full terms.