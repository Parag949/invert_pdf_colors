from pathlib import Path
from typing import Iterable, List
from natsort import natsorted


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def list_images(directory: Path, extensions: Iterable[str] = (".jpg", ".jpeg", ".png")) -> List[Path]:
    files = [f for f in directory.iterdir() if f.suffix.lower() in extensions]
    return list(map(Path, natsorted([str(f) for f in files])))
