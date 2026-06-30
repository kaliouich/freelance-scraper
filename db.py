import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "missions.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            url TEXT,
            platform TEXT,
            date_published TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_mission_exists(mission_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM missions WHERE id = ?", (mission_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_mission(mission_id: str, title: str, company: str, url: str, platform: str, date_published: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO missions (id, title, company, url, platform, date_published) VALUES (?, ?, ?, ?, ?, ?)",
        (mission_id, title, company, url, platform, date_published)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
