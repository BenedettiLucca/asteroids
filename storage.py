import os
import pathlib

APP_NAME = "asteroids"
DATA_DIR = pathlib.Path(os.environ.get("XDG_DATA_HOME", pathlib.Path.home() / ".local" / "share")) / APP_NAME
HIGHSCORE_FILE = DATA_DIR / "highscore.txt"


def load_highscore() -> int:
    """Load the high score from the storage file."""
    if not HIGHSCORE_FILE.exists():
        save_highscore(0)
        return 0
    try:
        content = HIGHSCORE_FILE.read_text().strip()
        return int(content) if content else 0
    except (ValueError, OSError):
        return 0


def save_highscore(score: int) -> None:
    """Save the high score to the storage file."""
    try:
        HIGHSCORE_FILE.parent.mkdir(parents=True, exist_ok=True)
        HIGHSCORE_FILE.write_text(str(score))
    except OSError:
        pass
