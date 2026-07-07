from database.connection import get_connection

def insert_weather(record):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO weather (city_id, temperature, humidity, wind_speed, observation_time)
        VALUES (?, ?, ?, ?, ?)
    ''',
        (record["city_id"],
        record["temperature"],
        record["humidity"],
        record["windspeed"],
        record["time"]))

    conn.commit()
    conn.close()