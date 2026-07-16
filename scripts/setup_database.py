from database.schema import create_city_table, create_weather_table

def main():
    create_city_table()
    create_weather_table()

if __name__ == "__main__":
    main()