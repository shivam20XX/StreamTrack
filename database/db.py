import sqlite3

DB_PATH = "database/streamtrack.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS library (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tmdb_id INTEGER,
        title TEXT,
        media_type TEXT,
        poster_path TEXT,
        status TEXT,
        rating REAL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    
def add_to_library(tmdb_id, title, media_type, poster_path, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO library (tmdb_id, title, media_type, poster_path, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (tmdb_id, title, media_type, poster_path, status)
    )

    conn.commit()
    conn.close()    