import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

_logger = logging.getLogger("invert_pdf_colors")
_logger.setLevel(logging.INFO)

_formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")

_console = logging.StreamHandler()
_console.setFormatter(_formatter)

_file = RotatingFileHandler(str(LOG_FILE), maxBytes=1_000_000, backupCount=3)
_file.setFormatter(_formatter)

if not _logger.handlers:
    _logger.addHandler(_console)
    _logger.addHandler(_file)


def get_logger() -> logging.Logger:
    return _logger
