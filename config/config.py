import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

CURRENT_PARAMS = os.getenv("CURRENT_PARAMS")

TIMEOUT= int(os.getenv("TIMEOUT"))

CITY_PATH = "data/cities.csv"

RAW_DATA_PATH = "data/raw/weather.csv"

LOG_PATH = "logs/weather.log"