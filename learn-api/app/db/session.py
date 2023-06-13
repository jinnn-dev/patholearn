from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

"""
Database connection configuration and connection creation
"""
engine = create_engine(
    settings.DATABASE_URL, pool_pre_ping=True, echo=False, echo_pool=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class SessionManager(object):
    def __init__(self):
        self.session: Session = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )()

    def __enter__(self):
        return self.session

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()


def close_session(session: Session):
    session.close()
