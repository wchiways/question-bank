import sqlite3
import os

DB_PATH = "question_bank.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print("Database not found, skipping migration.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if usage_count exists
        cursor.execute("PRAGMA table_info(api_keys)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'usage_count' not in columns:
            print("Adding usage_count column...")
            cursor.execute("ALTER TABLE api_keys ADD COLUMN usage_count INTEGER DEFAULT 0")
        
        if 'last_used_at' not in columns:
            print("Adding last_used_at column...")
            cursor.execute("ALTER TABLE api_keys ADD COLUMN last_used_at DATETIME")

        conn.commit()
        print("Migration completed successfully.")
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
