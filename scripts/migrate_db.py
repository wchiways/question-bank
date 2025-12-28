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
        # Check existing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Existing tables: {tables}")

        # Create provider_stats table if not exists
        if 'provider_stats' not in tables:
            print("Creating provider_stats table...")
            cursor.execute("""
                CREATE TABLE provider_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provider_name VARCHAR NOT NULL,
                    call_count INTEGER DEFAULT 0,
                    last_called_at DATETIME
                )
            """)
            # Create index
            cursor.execute("CREATE INDEX ix_provider_stats_provider_name ON provider_stats (provider_name)")
            print("✅ provider_stats table created")

        # Create call_logs table if not exists
        if 'call_logs' not in tables:
            print("Creating call_logs table...")
            cursor.execute("""
                CREATE TABLE call_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provider VARCHAR NOT NULL,
                    model VARCHAR,
                    prompt_length INTEGER,
                    response_length INTEGER,
                    latency_ms INTEGER,
                    success BOOLEAN DEFAULT 1,
                    error_message TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ call_logs table created")

        # Check if api_keys table exists and add columns if needed
        if 'api_keys' in tables:
            cursor.execute("PRAGMA table_info(api_keys)")
            columns = [info[1] for info in cursor.fetchall()]
            
            if 'usage_count' not in columns:
                print("Adding usage_count column to api_keys...")
                cursor.execute("ALTER TABLE api_keys ADD COLUMN usage_count INTEGER DEFAULT 0")
            
            if 'last_used_at' not in columns:
                print("Adding last_used_at column to api_keys...")
                cursor.execute("ALTER TABLE api_keys ADD COLUMN last_used_at DATETIME")
        else:
            print("Creating api_keys table...")
            cursor.execute("""
                CREATE TABLE api_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key VARCHAR NOT NULL UNIQUE,
                    name VARCHAR DEFAULT 'Default',
                    enabled BOOLEAN DEFAULT 1,
                    usage_count INTEGER DEFAULT 0,
                    last_used_at DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ api_keys table created")

        conn.commit()
        print("✅ Migration completed successfully.")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
