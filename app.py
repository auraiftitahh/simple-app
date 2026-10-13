import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify

app = Flask(__name__)
database = Path(os.environ.get('DATABASE_PATH', '/data/app.db'))


@app.get('/')
def hello():
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database, timeout=30) as connection:
        connection.execute('CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY, created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
        connection.execute('INSERT INTO visits DEFAULT VALUES')
        count = connection.execute('SELECT COUNT(*) FROM visits').fetchone()[0]
    return jsonify(message='Halo dari Flask + SQLite + Docker + Jenkins!', visits=count)


@app.get('/health')
def health():
    return jsonify(status='ok')
