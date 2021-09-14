from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.utils.colored_printer import ColoredPrinter


def init() -> None:
    """
    Initializes Database
    """
    db = SessionLocal()
    init_db(db)


def main() -> None:
    ColoredPrinter.print_info("Creating initial data")
    init()
    ColoredPrinter.print_info("Initial data created")


if __name__ == "__main__":
    main()
