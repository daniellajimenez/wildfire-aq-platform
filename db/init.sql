CREATE EXTENSION IF NOT EXISTS timescaledb;

-- create table
CREATE TABLE IF NOT EXISTS agrimonia_daily (
  date        DATE        PRIMARY KEY,
  pm25        DOUBLE PRECISION,
  pm10        DOUBLE PRECISION,
  no2         DOUBLE PRECISION,
  co          DOUBLE PRECISION,
  nh3         DOUBLE PRECISION,
  so2         DOUBLE PRECISION,
  temp_c      DOUBLE PRECISION,
  humidity    DOUBLE PRECISION,
  wind_m_s    DOUBLE PRECISION,
  precip_mm   DOUBLE PRECISION,
  press_hPa   DOUBLE PRECISION
);

-- turn table into a hypertable
SELECT create_hypertable('agrimonia_daily', 'date', if_not_exists => TRUE);

-- bulk‐load the CSV into table
COPY agrimonia_daily
  FROM '/docker-entrypoint-initdb.d/agrimonia_daily.csv'
  WITH (FORMAT csv, HEADER true);
