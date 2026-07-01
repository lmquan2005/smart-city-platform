from config.config import CITY_PATH
from extract.weather_api import extract_weather
from transform.weather_transform import transform_weather
from load.csv_loader import save_csv
import pandas as pd
from config.logger import logging
from load.city_loader import load_city

def main():
    cities = load_city(CITY_PATH)
    for _, city in cities.iterrows():
        latitude = city["latitude"]
        longitude = city["longitude"]
        
        logging.info(f"Bắt đầu xử lý dữ liệu thời tiết cho thành phố: {city['city']}")
        weather = extract_weather(latitude, longitude)
        if weather is None:
            logging.error(f"Không thể lấy dữ liệu thời tiết cho thành phố: {city['city']}. Bỏ qua.")
            continue

        df = transform_weather(weather, city['city'])
        if df is None or df.empty:
            logging.error(f"Không thể chuyển đổi dữ liệu thời tiết cho thành phố: {city['city']}. Bỏ qua.")
            continue

        save_csv(df)
        logging.info(f"Hoàn tất xử lý dữ liệu thời tiết cho thành phố: {city['city']}")

if __name__ == "__main__":
    main() 
