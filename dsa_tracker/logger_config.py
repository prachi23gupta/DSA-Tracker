import logging
from pathlib import Path


LOG_DIRECTORY = (
    Path(__file__).resolve().parent.parent / "logs"
)

LOG_FILE = LOG_DIRECTORY / "dsa_tracker.log"


def setup_logging() -> None:
    """Configure application logging."""

    LOG_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8",
            ),
        ],
    )