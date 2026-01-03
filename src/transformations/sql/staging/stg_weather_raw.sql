CREATE TABLE IF NOT EXISTS staging.weather_raw (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(100),
    temperature FLOAT,
    humidity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
