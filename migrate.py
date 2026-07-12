import sqlite3
import sys

DB_PATH = "./shelf.db"

# Add new migrations to the end of this list.
# Each entry must be idempotent-safe (duplicate column errors are handled automatically).
migrations = [
    "ALTER TABLE films ADD COLUMN type TEXT",
    "UPDATE films SET type = 'Film' WHERE type IS NULL OR TRIM(type) = ''",
]


def run():
    conn = sqlite3.connect(DB_PATH)
    for sql in migrations:
        try:
            conn.execute(sql)
            conn.commit()
            print(f"Applied: {sql}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e):
                print(f"Skipped (already applied): {sql}")
            else:
                print(f"Error running migration: {e}", file=sys.stderr)
                conn.close()
                sys.exit(1)
    conn.close()
    print("Migrations complete.")


if __name__ == "__main__":
    run()
