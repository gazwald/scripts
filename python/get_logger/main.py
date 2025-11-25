from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger


def get_logger(
    name: str | None = None,
    log_level: str = "INFO",
) -> Logger:
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), "NOTSET"),
        format=" | ".join(
            [
                "%(asctime)s",
                "%(module)-10s",
                "%(funcName)-20s",
                "%(levelname)-10s",
                "%(message)s",
            ]
        ),
    )
    return logging.getLogger(name or __name__)
