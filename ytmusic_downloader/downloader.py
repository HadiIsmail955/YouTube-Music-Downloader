import subprocess
import os
import yaml


def load_config():
    with open("config/config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_paths(cfg):
    os.makedirs(cfg["download_dir"], exist_ok=True)
    os.makedirs(os.path.dirname(cfg["archive_file"]), exist_ok=True)


def sanitize(name: str) -> str:
    return (
        name.replace("/", "_")
        .replace("\\", "_")
        .replace(":", " -")
        .strip()
    )


def download(url, fallback_artist):
    cfg = load_config()
    ensure_paths(cfg)

    safe_artist = sanitize(fallback_artist)

    print(f"\n▶ Downloading:\n{url}")
    print(f"   Artist folder: {safe_artist}")

    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", cfg["audio_format"],
        "--download-archive", cfg["archive_file"],
        "--embed-metadata",
        "--parse-metadata", f"album_artist:{safe_artist}",
        "--parse-metadata", "artist:%(artist)s",
        "--embed-thumbnail",
        "--retries", str(cfg.get("retries", 10)),
        "--socket-timeout", str(cfg.get("socket_timeout", 30)),
        "--progress",
        "-o",
        f"{cfg['download_dir']}/{safe_artist}/%(album)s/%(title)s.%(ext)s",

        url
    ]
    
    cmd.extend([
        "--concurrent-fragments",
        str(cfg.get("concurrent_fragments", 4))
    ])

    if cfg.get("limit_rate"):
        cmd.extend(["--limit-rate", cfg["limit_rate"]])

    # Behavior
    if cfg.get("skip_existing", True):
        cmd.append("--no-overwrites")

    if cfg.get("continue_downloads", True):
        cmd.append("--continue")

    subprocess.run(cmd)
