from database.connection import get_connection

def insert_city_data(record):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO city (city, latitude, longitude)
        VALUES (%s, %s, %s)
        ON CONFLICT(city) DO NOTHING
    ''',(record["city"], record["latitude"], record["longitude"]))

    conn.commit()
    conn.close()

def insert_weather_data(record):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO weather (city_id, observation_time, temperature, humidity, wind_speed)
        VALUES (%s, %s, %s, %s, %s)
    ''', (record["city_id"], record["observation_time"], record["temperature"], record["humidity"], record["wind_speed"]))
    conn.commit()
    conn.close()

def get_city_id(city_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM city WHERE city = %s', (city_name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None