-- create base tables
CREATE TABLE agrimonia (
  date      DATE       PRIMARY KEY,
  pm25      DOUBLE PRECISION,
  pm10      DOUBLE PRECISION,
  no2       DOUBLE PRECISION,
  co        DOUBLE PRECISION,
  nh3       DOUBLE PRECISION,
  temp_c    DOUBLE PRECISION,
  humidity  DOUBLE PRECISION,
  wind_m_s  DOUBLE PRECISION,
  precip_mm DOUBLE PRECISION,
  press_hPa DOUBLE PRECISION
);

CREATE TABLE fires (
  date       DATE       PRIMARY KEY,
  fire_count INTEGER,
  avg_frp    DOUBLE PRECISION
);

-- convert both into hypertables
SELECT create_hypertable('agrimonia', 'date', if_not_exists => TRUE);
SELECT create_hypertable('fires',     'date', if_not_exists => TRUE);
