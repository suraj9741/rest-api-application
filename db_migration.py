import psycopg2
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration using environment variables
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT")
}
# Folder where migration SQL files are stored
MIGRATIONS_DIR = "migrations"

# Create a database connection
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# Create migration tracking table if it does not exist
def ensure_migration_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS schema_migrations (
        version VARCHAR(50) PRIMARY KEY,
        applied_at TIMESTAMP NOT NULL
    )
    """)

# Get already applied migrations from DB
def get_applied_migrations(cur):
    cur.execute("SELECT version FROM schema_migrations")
    return {row[0] for row in cur.fetchall()}

# Get list of migration SQL files
def get_migration_files():
    files = [f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql")]
    files.sort()
    return files

# Execute a single migration
def run_migration(cur, version, filepath):
    print(f"Applying migration: {filepath}")

    with open(filepath, "r") as f:
        sql = f.read()

    cur.execute(sql)

    cur.execute(
        "INSERT INTO schema_migrations (version, applied_at) VALUES (%s, %s)",
        (version, datetime.utcnow())
    )

# Main migration runner
def migrate():
    conn = None

    try:
        # Open database connection
        conn = get_connection()
        cur = conn.cursor()
        
        # Ensure migration tracking table exists
        ensure_migration_table(cur)
        conn.commit()

        # Get already applied migrations
        applied = get_applied_migrations(cur)

        # Get migration files from directory
        files = get_migration_files()

        # Loop through migration files and apply those that haven't been applied yet
        for file in files:

            version = file.split("_")[0]
            # Skip already applied migrations
            if version in applied:
                continue

            filepath = os.path.join(MIGRATIONS_DIR, file)

            try:
                # Run migration and commit changes
                run_migration(cur, version, filepath)
                conn.commit()

            # Rollback if migration fails
            except Exception as migration_error:
                conn.rollback()
                print(f"Migration failed: {file}")
                print(migration_error)
                sys.exit(1)

        print("All migrations applied successfully")

    except Exception as e:
        print("Database connection error:", e)

    finally:
        # Always close connection
        if conn:
            conn.close()


if __name__ == "__main__":
    migrate()