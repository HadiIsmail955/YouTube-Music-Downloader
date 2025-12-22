import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.yml"

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing config: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # 🔒 Normalize paths to ABSOLUTE
    cfg["download_dir"] = str((BASE_DIR / cfg["download_dir"]).resolve())
    cfg["archive_file"] = str((BASE_DIR / cfg["archive_file"]).resolve())

    return cfg
