import sqlite3
import os
import glob
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database file path
database_name = "database.sqlite"

def create_tables_from_sql_files():
    """Load and execute all SQL files in the tables directory"""

    # Connect to SQLite database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Find all .sql files in the tables directory
    sql_files = glob.glob("sql/tables/*.sql")

    if not sql_files:
        logger.warning("No SQL files found in sql/tables/ directory")
        return

    logger.info(f"Found {len(sql_files)} SQL file(s) to process:")

    for sql_file in sql_files:
        logger.info(f"Processing: {sql_file}")

        try:
            # Read the SQL file
            with open(sql_file, 'r') as f:
                sql_content = f.read()

            # Execute the SQL commands
            cursor.executescript(sql_content)
            logger.info(f"✓ Successfully executed {os.path.basename(sql_file)}")

        except Exception as e:
            logger.error(f"✗ Error executing {os.path.basename(sql_file)}: {e}")

    # Commit changes and close connection
    conn.commit()
    conn.close()

    logger.info(f"Database '{database_name}' is ready with all tables!")

if __name__ == "__main__":
    create_tables_from_sql_files()