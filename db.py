import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def connect():
    
    conn = sqlite3.connect('users.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        feature TEXT NOT NULL,
        input_text TEXT NOT NULL,
        result TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    return conn

def add_user(username, email, password):
    conn = connect()
    try:
        conn.execute('INSERT INTO users VALUES (?, ?, ?)',
                     (email, username, generate_password_hash(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(email, password):
    conn = connect()
    row = conn.execute('SELECT password FROM users WHERE email = ?',
                       (email,)).fetchone()
    conn.close()
    return row is not None and check_password_hash(row[0], password)

def save_history(email, feature, input_text, result):
    conn = connect()
    conn.execute('INSERT INTO history (email, feature, input_text, result) VALUES (?, ?, ?, ?)',
                 (email, feature, input_text, result))
    conn.commit()
    conn.close()

def get_history(email):
    conn = connect()
    rows = conn.execute('SELECT feature, input_text, result, created_at FROM history WHERE email = ? ORDER BY id DESC',
                        (email,)).fetchall()
    conn.close()
    return rows