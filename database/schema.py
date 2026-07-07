from database.connection import get_connection

def create_city_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS city (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
    
def create_weather_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER KEY REFERENCES city(id),
        observation_time TEXT NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        wind_speed REAL NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

