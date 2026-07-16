from numpy import record

from config.config import CITY_PATH
from src.extract.weather_api import extract_weather
from src.transform.weather_transform import transform_weather
from src.load.csv_loader import save_csv
import pandas as pd
from config.logger import logging
from src.load.city_loader import load_city
from database.repository import insert_city_data, get_city_id, insert_weather_data

def main():
    cities = load_city(CITY_PATH)

    for _, city in cities.iterrows():
        insert_city_data(city)

    for _, city in cities.iterrows():
        latitude = city["latitude"]
        longitude = city["longitude"]
        
        logging.info(f"Bắt đầu xử lý dữ liệu thời tiết cho thành phố: {city['city']}")

        weather = extract_weather(latitude, longitude)
        if weather is None:
            logging.error(f"Không thể lấy dữ liệu thời tiết cho thành phố: {city['city']}. Bỏ qua.")
            continue

        records = transform_weather(weather, city['city'])  

        city_id = get_city_id(records["city"])
        records["city_id"] = city_id

        df = pd.DataFrame([records]) if records else pd.DataFrame()
        if df is None or df.empty:
            logging.error(f"Không thể chuyển đổi dữ liệu thời tiết cho thành phố: {city['city']}. Bỏ qua.")
            continue

        save_csv(df)
        insert_weather_data(records)

        logging.info(f"Hoàn tất xử lý dữ liệu thời tiết cho thành phố: {city['city']}")

if __name__ == "__main__":
    main() 
