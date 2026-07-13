import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Get log level from environment variable, default to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Create root logger
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)

# Log format with more detailed info
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console handler (stdout)
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(log_format)
root_logger.addHandler(console_handler)

# File handler with rotation
file_handler = RotatingFileHandler(
    LOGS_DIR / "app.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5  # Keep 5 backup files
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(log_format)
root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logging.getLogger(name)
