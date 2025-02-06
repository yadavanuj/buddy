import sqlite3

def connect_db():
    return sqlite3.connect('./buddy_db/buddy_cli.db')

def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS state (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                value TEXT NOT NULL
            )
        ''')
        conn.commit()

def insert_state(name, value):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO state (name, value) VALUES (?, ?)', (name, value))
        conn.commit()

def get_state(name):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM state WHERE name = ?', (name,))
        return cursor.fetchone()

def update_state(name, value):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE state SET value = ? WHERE name = ?', (value, name))
        conn.commit()

def delete_state(name):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM state WHERE name = ?', (name,))
        conn.commit()
