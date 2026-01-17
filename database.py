
import sqlite3

conn = sqlite3.connect("stats.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    games INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    impostor_wins INTEGER DEFAULT 0
)
""")

conn.commit()
