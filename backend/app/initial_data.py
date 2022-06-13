from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.utils.logger import logger
from app.utils.timer import Timer


def init() -> None:
    """
    Initializes Database
    """
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    timer = Timer()
    timer.start()
    init()
    timer.stop()
    logger.info(f"Initial data created in {timer.total_run_time}s")


if __name__ == "__main__":
    main()
