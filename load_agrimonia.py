import pandas as pd
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dani@localhost:5432/aq")

# path to daily CSV
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "agrimonia_daily.csv")

def main():
    # load CSV
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    print(f"🔍 CSV rows: {len(df)} • columns: {list(df.columns)}")

    # connect
    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        # drop & recreate a plain table
        conn.execute(text("DROP TABLE IF EXISTS agrimonia"))
        # write via pandas
        df.to_sql("agrimonia", conn, index=False)
        print("Loaded into Postgres table: agrimonia")

if __name__ == "__main__":
    main()

