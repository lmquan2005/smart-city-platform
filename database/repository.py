from database.connection import get_connection
from database.queries import GET_CITY_ID, INSERT_CITY, INSERT_WEATHER
from config.logger import logging

def insert_city_data(record):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(INSERT_CITY, (record["city"], record["latitude"], record["longitude"]))
        conn.commit()
        conn.close()

        logging.info("City data inserted successfully.")
    except Exception as e:
        logging.error(f"Error inserting city data: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def get_city_id(city_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(GET_CITY_ID, (city_name,))
        result = cursor.fetchone()

        logging.info(f"Fetched city ID for {city_name}: {result[0] if result else None}")
        return result[0] if result else None
    
    except Exception as e:
        logging.error(f"Error fetching city ID: {e}")
        raise
    finally:
        if conn:
            conn.close()


def insert_weather_data(record):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(INSERT_WEATHER, (record["city_id"], record["observation_time"], record["temperature"], record["humidity"], record["wind_speed"]))
        conn.commit()
        logging.info(f"Weather data inserted successfully for city ID {record['city_id']}.")
    except Exception as e:
        logging.error(f"Error inserting weather data: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

