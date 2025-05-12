COPY agrimonia FROM '/docker-entrypoint-initdb.d/../../data/agrimonia_daily.csv'
  WITH (FORMAT csv, HEADER);
