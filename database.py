import sqlite3


def create_database():
    conn = sqlite3.connect("dahel.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            training TEXT,
            training_type TEXT,
            experience TEXT,
            location TEXT,
            start_date TEXT,
            goal TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()
