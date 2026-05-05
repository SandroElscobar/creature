import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

conn: Connection | None = None
cursor: Cursor | None = None

def get_db(name: str|None = None, reset: bool = False):
    """Подключаемся к файлу БД"""
    global conn, cursor
    if conn:
        if not reset:
            return
        conn = None

    if not name:
        name = os.getenv("CRYPTID_SQLITE_DB")
        top_dir = Path(__file__).resolve().parents[1]
        db_dir = top_dir / "data"
        db_name = "cryptid.db"
        db_path = db_dir / db_name
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)

    conn = connect(name, check_same_thread=False)
    cursor = conn.cursor()

get_db()