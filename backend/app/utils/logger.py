import sys

import loguru

logger = loguru.logger

logger.configure(handlers=[{"sink": sys.stderr, "colorize": True}])
