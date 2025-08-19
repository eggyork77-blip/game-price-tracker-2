import sqlite3

DB_FILE = "cdkeys_prices.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cdkeys_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            game_name TEXT NOT NULL,
            price REAL NOT NULL,
            currency TEXT,
            url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ สร้าง {DB_FILE} และตาราง cdkeys_prices แล้ว")

if __name__ == "__main__":
    init_db()