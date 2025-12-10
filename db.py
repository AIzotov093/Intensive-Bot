# db.py
import sqlite3
from typing import Optional, Tuple

DB_NAME = "messages.db"

def init_db() -> None:
    """Инициализировать базу и создать таблицу messages при необходимости."""
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                sender TEXT,
                text TEXT,
                date TEXT
            );
            """
        )
        conn.commit()
    finally:
        conn.close()

def get_message_by_id(msg_id: int) -> Optional[Tuple]:
    """Проверить, есть ли сообщение с таким id (для проверки дублей)."""
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages WHERE id = ?", (msg_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def save_message(msg_id: int, chat_id: int, sender: Optional[str], text: Optional[str], date: str) -> None:
    """Сохранить сообщение в БД, избегая дублей по id."""
    if get_message_by_id(msg_id) is not None:
        return
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (id, chat_id, sender, text, date) VALUES (?, ?, ?, ?, ?)", (msg_id, chat_id, sender, text, date))
        conn.commit()
    finally:
        conn.close()
