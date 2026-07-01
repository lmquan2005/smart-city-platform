import pandas as pd
from config.logger import logging


def load_city(path):
    return pd.read_csv(path)
