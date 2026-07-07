import sqlite3

DATABASE_PATH = 'database/weather.db'

def get_connection():
    return sqlite3.connect(DATABASE_PATH)