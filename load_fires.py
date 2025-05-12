import os
import pandas as pd
from sqlalchemy import create_engine, text

# paths
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "agrimonia_fire_counts_daily.csv")

# load CSV
fires = pd.read_csv(DATA_FILE, parse_dates=["date"])
print(f"🔍 CSV rows: {len(fires)} • columns: {list(fires.columns)}")

# connect
engine = create_engine("postgresql://postgres:postgres@localhost:5432/aq")

with engine.begin() as conn:
    # drop & recreate table with date primary key
    conn.execute(text("DROP TABLE IF EXISTS fires;"))
    conn.execute(text("""
      CREATE TABLE fires (
        date       DATE      PRIMARY KEY,
        fire_count INTEGER,
        avg_frp    DOUBLE PRECISION
      );
    """))

    # turn it into a Timescale hypertable
    conn.execute(text("SELECT create_hypertable('fires','date');"))

    # bulk‐insert all rows
    fires.to_sql("fires", conn, if_exists="append", index=False, method="multi", chunksize=500)

    print("Loaded fire counts into `fires` hypertable")



