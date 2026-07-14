from database.connection import get_connection

def create_city_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS city (
        id SERIAL PRIMARY KEY,
        city VARCHAR(100) UNIQUE NOT NULL,
        latitude DOUBLE PRECISION NOT NULL,
        longitude DOUBLE PRECISION NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
    
def create_weather_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id SERIAL PRIMARY KEY,
        city_id INTEGER REFERENCES city(id),
        observation_time TIMESTAMP NOT NULL,
        temperature DOUBLE PRECISION NOT NULL,
        humidity DOUBLE PRECISION NOT NULL,
        wind_speed DOUBLE PRECISION NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

