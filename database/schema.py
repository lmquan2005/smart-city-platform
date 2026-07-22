from database.connection import get_connection
from database.queries import CREATE_CITY_TABLE, CREATE_WEATHER_TABLE
from config.logger import logging

def create_city_table():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(CREATE_CITY_TABLE)
        conn.commit()
        logging.info("City table created successfully.")
    except Exception as e:
        logging.error(f"Error creating city table: {e}")
    finally:
        if conn is not None:    
            conn.close()
            
def create_weather_table():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(CREATE_WEATHER_TABLE)
        conn.commit()
        logging.info("Weather table created successfully.")
    except Exception as e:
        logging.error(f"Error creating weather table: {e}")
    finally:
        if conn is not None:
            conn.close()


