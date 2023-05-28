import sys

import loguru

logger = loguru.logger

logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "colorize": True,
        }
    ]
)
