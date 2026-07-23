from database.schema import create_city_table, create_weather_table, create_database

def main():
    create_database()
    create_city_table()
    create_weather_table()

if __name__ == "__main__":
    main()