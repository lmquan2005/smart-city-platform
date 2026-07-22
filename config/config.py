import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

CURRENT_PARAMS = os.getenv("CURRENT_PARAMS")

TIMEOUT= int(os.getenv("TIMEOUT"))

CITY_PATH = "data/cities.csv"

RAW_DATA_PATH = "data/raw/weather.csv"

LOG_PATH = "logs/weather.log"

DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION")
