from database.connection import get_connection

def seed_city_data(record):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO city (city, latitude, longitude)
        VALUES (?, ?, ?)
    ''',(record["city"], record["latitude"], record["longitude"]))

    conn.commit()
    conn.close()