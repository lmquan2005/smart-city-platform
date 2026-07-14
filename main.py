from config.config import CITY_PATH
from extract.weather_api import extract_weather
from transform.weather_transform import transform_weather
from load.csv_loader import save_csv
import pandas as pd
from config.logger import logging
from load.city_loader import load_city
from load.sqlite_loader import insert_weather
from database.schema import create_weather_table, create_city_table
from database.seed import seed_city_data

def main():
    create_city_table()
    create_weather_table()

    cities = load_city(CITY_PATH)
    for _, city in cities.iterrows():
        seed_city_data(city) 
        latitude = city["latitude"]
        longitude = city["longitude"]
        
        logging.info(f"Bắt đầu xử lý dữ liệu thời tiết cho thành phố: {city['city']}")

        weather = extract_weather(latitude, longitude)
        if weather is None:
            logging.error(f"Không thể lấy dữ liệu thời tiết cho thành phố: {city['city']}. Bỏ qua.")
            continue

        records = transform_weather(weather, city['city'])
        df = pd.DataFrame([records]) if records else pd.DataFrame()
        if df is None or df.empty:
            logging.error(f"Không thể chuyển đổi dữ liệu thời tiết cho thành phố: {city['city']}. Bỏ qua.")
            continue

        save_csv(df)

        for _, row in df.iterrows():
            insert_weather(row.to_dict())
        logging.info(f"Hoàn tất xử lý dữ liệu thời tiết cho thành phố: {city['city']}")

if __name__ == "__main__":
    main() 
