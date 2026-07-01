import pandas as pd
from config.logger import logging

def transform_weather(weather, city):
    try:
        record = {
            "city": city,
            "time": weather["current"]["time"],
            "temperature": weather["current"]["temperature_2m"],
            "humidity": weather["current"]["relative_humidity_2m"],
            "windspeed": weather["current"]["wind_speed_10m"],
            "latitude": weather["latitude"],
            "longitude": weather["longitude"]
        }
        return pd.DataFrame([record])
    except KeyError as e:
        logging.error(f"Lỗi khi chuyển đổi dữ liệu thời tiết: {e}")
        return None  # Return an empty DataFrame in case of error
