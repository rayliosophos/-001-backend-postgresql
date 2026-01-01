import sys
import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "%(filename)s:%(lineno)d | %(message)s"
)

MAX_LOG_SIZE = 20 * 1024 * 1024  # 20 MB


class SizeAndTimeRotatingHandler(TimedRotatingFileHandler):
    """
    Rotate logs daily AND when file exceeds MAX_LOG_SIZE.
    """

    def shouldRollover(self, record):
        # Time-based rollover
        if super().shouldRollover(record):
            return True

        # Size-based rollover
        if self.stream:
            self.stream.seek(0, 2)  # go to end of file
            if self.stream.tell() >= MAX_LOG_SIZE:
                return True

        return False


def setup_logging(level: str = "INFO") -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)

    formatter = logging.Formatter(LOG_FORMAT)

    # Console handler (Docker / dev)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # File handler (production)
    file_handler = SizeAndTimeRotatingHandler(
        filename=str(LOG_FILE),
        when="midnight",     # rotate daily
        interval=1,
        backupCount=14,      # keep 14 days
        encoding="utf-8",
        utc=False,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # IMPORTANT: avoid duplicate logs
    root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("asyncpg").setLevel(logging.WARNING)
    logging.getLogger("asyncpg.pool").setLevel(logging.WARNING)
    logging.getLogger("asyncpg.connection").setLevel(logging.WARNING)
    logging.getLogger("oracledb").setLevel(logging.WARNING)

    root_logger.info("✅ Logging initialized (daily + 20MB rotation)")
