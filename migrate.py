import sqlite3
import sys
from logger import get_logger

logger = get_logger(__name__)

DB_PATH = "./shelf.db"

# Add new migrations to the end of this list.
# Each entry must be idempotent-safe (duplicate column errors are handled automatically).
migrations = [
    "ALTER TABLE films ADD COLUMN type TEXT",
    "UPDATE films SET type = 'Film' WHERE type IS NULL OR TRIM(type) = ''",
]


def run():
    logger.info("Starting database migrations...")
    conn = sqlite3.connect(DB_PATH)
    for sql in migrations:
        try:
            conn.execute(sql)
            conn.commit()
            logger.info(f"Applied: {sql}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e):
                logger.info(f"Skipped (already applied): {sql}")
            else:
                logger.error(f"Error running migration: {e}")
                conn.close()
                logger.critical("Migration failed. Exiting.")
                sys.exit(1)
    conn.close()
    logger.info("Migrations complete.")


if __name__ == "__main__":
    run()
