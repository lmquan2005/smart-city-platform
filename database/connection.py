import psycopg2
import config.config as config

def get_connection():
    return psycopg2.connect(
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )