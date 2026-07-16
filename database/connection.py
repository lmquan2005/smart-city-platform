import psycopg2
import config.config as config
from config.logger import logging

def get_connection():
    try:
        conn = psycopg2.connect(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME
        )

        logging.info("Connected to PostgreSQL")

        return conn
    except Exception as e:
        logging.error(f"Cannot connect to PostgreSQL: {e}")
        raise