import requests
from config.logger import logging
from config.config import CURRENT_PARAMS, BASE_URL, TIMEOUT

def extract_weather(latitude , longitude):
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": CURRENT_PARAMS
        }

        logging.info("Bắt đầu lấy dữ liệu thời tiết")
        
        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi khi lấy dữ liệu thời tiết: {e}")
        return None
