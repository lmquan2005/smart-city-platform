CREATE_DATABASE = """
CREATE DATABASE IF NOT EXISTS weather_db
"""

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

GET_LATEST_DATA_WEATHER = """
SELECT c.city, w.temperature, w.humidity, w.wind_speed, w.observation_time
FROM city AS c
INNER JOIN weather AS w ON c.id = w.city_id
WHERE w.observation_time = (
    SELECT MAX(observation_time) FROM weather WHERE city_id = c.id
)
ORDER BY c.city
"""

GET_SUMMARY_DATA = """
SELECT
    COUNT(DISTINCT c.id),
    ROUND(AVG(w.temperature)::numeric, 2) AS avg_temperature,
    ROUND(AVG(w.humidity)::numeric, 2) AS avg_humidity,
    ROUND(AVG(w.wind_speed)::numeric, 2) AS avg_wind_speed,
    MAX(w.observation_time)
FROM city AS c
INNER JOIN weather AS w ON c.id = w.city_id
"""

GET_LATEST_TEMPERATURE = """
SELECT c.city, w.temperature
FROM city AS c
INNER JOIN weather AS w ON c.id = w.city_id
WHERE w.observation_time = (
    SELECT MAX(observation_time) FROM weather WHERE city_id = c.id
)
ORDER BY c.city
"""

GET_WEATHER_DATA = """
SELECT
    c.city,
    w.temperature,
    w.humidity,
    w.wind_speed,
    w.observation_time
FROM weather w
JOIN city c ON c.id = w.city_id
ORDER BY w.observation_time DESC
LIMIT %s OFFSET %s
"""
GET_WEATHER_DATA_BY_CITY = """
SELECT
    c.city,
    w.temperature,
    w.humidity,
    w.wind_speed,
    w.observation_time
FROM city AS c
INNER JOIN weather AS w ON c.id = w.city_id
WHERE c.city = %s
ORDER BY w.observation_time DESC
"""

GET_DATA_WEATHER_BY_DATE = """
SELECT c.city, w.temperature, w.humidity, w.wind_speed, w.observation_time
FROM city AS c
INNER JOIN weather AS w ON c.id = w.city_id
WHERE w.observation_time::date = %s::date
ORDER BY w.observation_time DESC
"""

GET_ALL_CITIES = """
SELECT city FROM city ORDER BY city
"""