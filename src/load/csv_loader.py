import os

import pandas as pd
from config.logger import logging
from config.config import RAW_DATA_PATH


def save_csv(df):
    try:
        df.to_csv(RAW_DATA_PATH, index=False, mode='a', header=not os.path.exists(RAW_DATA_PATH))
        logging.info("Dữ liệu thời tiết đã được lưu")
    except Exception as e:
        logging.error(f"Lỗi khi lưu dữ liệu thời tiết: {e}")
