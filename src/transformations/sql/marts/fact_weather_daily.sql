CREATE TABLE IF NOT EXISTS marts.fact_weather_daily (
    date_key DATE PRIMARY KEY,
    location_key INT,
    temperature_avg FLOAT,
    humidity_avg FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
