from database.connection import get_connection
from database.queries import (
    GET_ALL_CITIES,
    GET_CITY_ID,
    GET_WEATHER_DATA_BY_CITY,
    GET_DATA_WEATHER_BY_DATE,
    GET_LATEST_DATA_WEATHER,
    GET_LATEST_TEMPERATURE,
    GET_SUMMARY_DATA,
    GET_WEATHER_DATA,
    INSERT_CITY,
    INSERT_WEATHER,
)
from config.logger import logging


def insert_city_data(record):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(INSERT_CITY, (record["city"], record["latitude"], record["longitude"]))
        conn.commit()

        logging.info("City data inserted successfully.")
    except Exception as e:
        logging.error(f"Error inserting city data: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def get_city_id(city_name):
    conn = None
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
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            INSERT_WEATHER,
            (
                record["city_id"],
                record["observation_time"],
                record["temperature"],
                record["humidity"],
                record["wind_speed"],
            ),
        )
        conn.commit()
        logging.info(f"Weather data inserted successfully for city ID {record['city_id']}.")
    except Exception as e:
        logging.error(f"Error inserting weather data: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def get_latest_weather():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(GET_LATEST_DATA_WEATHER)
        rows = cursor.fetchall()

        return [
            {
                "city": row[0],
                "temperature": row[1],
                "humidity": row[2],
                "wind_speed": row[3],
                "observation_time": row[4],
            }
            for row in rows
        ]
    except Exception as e:
        logging.error(f"Error fetching latest weather: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_dashboard_summary():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(GET_SUMMARY_DATA)
        rows = cursor.fetchall()

        return [
            {
                "total_city": row[0],
                "avg_temp": row[1],
                "avg_humidity": row[2],
                "avg_wind_speed": row[3],
                "last_updated": row[4],
            }
            for row in rows
        ]
    except Exception as e:
        logging.error(f"Error fetching dashboard summary: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_temperature_by_city():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(GET_LATEST_TEMPERATURE)
        rows = cursor.fetchall()

        return [
            {
                "city": row[0],
                "temperature": row[1],
            }
            for row in rows
        ]
    except Exception as e:
        logging.error(f"Error fetching temperature by city: {e}")
        raise
    finally:
        if conn:
            conn.close()


def _build_history_filters(city=None, date=None):
    conditions = []
    params = []

    if city:
        conditions.append("c.city = %s")
        params.append(city)

    if date:
        conditions.append("w.observation_time::date = %s::date")
        params.append(date)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    return where_clause, params


def _map_weather_rows(rows):
    return [
        {
            "city": row[0],
            "temperature": row[1],
            "humidity": row[2],
            "wind_speed": row[3],
            "observation_time": row[4],
        }
        for row in rows
    ]


def get_all_cities():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(GET_ALL_CITIES)
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logging.error(f"Error fetching cities: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_weather_history(limit=10, offset=0, city=None, date=None):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        where_clause, params = _build_history_filters(city, date)
        query = f"""
            SELECT
                c.city,
                w.temperature,
                w.humidity,
                w.wind_speed,
                w.observation_time
            FROM weather w
            JOIN city c ON c.id = w.city_id
            {where_clause}
            ORDER BY w.observation_time DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (*params, limit, offset))
        return _map_weather_rows(cursor.fetchall())
    finally:
        if conn:
            conn.close()


def count_weather(city=None, date=None):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        where_clause, params = _build_history_filters(city, date)
        query = f"""
            SELECT COUNT(*)
            FROM weather w
            JOIN city c ON c.id = w.city_id
            {where_clause}
        """
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    finally:
        if conn:
            conn.close()

def get_data_weather_by_city(city_name):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(GET_WEATHER_DATA_BY_CITY, (city_name,))
        result = cursor.fetchone()

        logging.info(f"Data weather by city: {result}")
        return result
    except Exception as e:
        logging.error(f"Error fetching data weather by city: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_data_weather_by_date(date):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(GET_DATA_WEATHER_BY_DATE, (date,))
        rows = cursor.fetchall()

        logging.info(f"Data weather by date: {len(rows)} rows")
        return _map_weather_rows(rows)
    except Exception as e:
        logging.error(f"Error fetching data weather by date: {e}")
        raise
    finally:
        if conn:
            conn.close()   


