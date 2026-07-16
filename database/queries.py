CREATE_CITY_TABLE = """
CREATE TABLE IF NOT EXISTS city (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) UNIQUE NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL
)"""

CREATE_WEATHER_TABLE = """
CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES city(id),
    observation_time TIMESTAMP NOT NULL,
    temperature DOUBLE PRECISION NOT NULL,
    humidity DOUBLE PRECISION NOT NULL,
    wind_speed DOUBLE PRECISION NOT NULL
)
"""

INSERT_CITY = """ 
INSERT INTO city (city, latitude, longitude)
    VALUES (%s, %s, %s)
    ON CONFLICT(city) DO NOTHING
"""
INSERT_WEATHER = """
INSERT INTO weather (city_id, observation_time, temperature, humidity, wind_speed)
    VALUES (%s, %s, %s, %s, %s)
"""

GET_CITY_ID = """
SELECT id FROM city WHERE city = %s
"""
