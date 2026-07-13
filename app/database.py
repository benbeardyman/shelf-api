from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.logger import get_logger

logger = get_logger(__name__)

DATABASE_URL = "sqlite:///./shelf.db"

logger.info(f"Initializing database engine with URL: {DATABASE_URL}")
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
logger.debug("Database engine created successfully")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.debug("SessionLocal sessionmaker configured")


class Base(DeclarativeBase):
    pass


def get_db():
    logger.debug("Creating new database session")
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error in database session: {str(e)}")
        raise
    finally:
        logger.debug("Closing database session")
        db.close()
