import joblib
import pandas as pd
from datetime import date as _date
from fastapi import FastAPI, HTTPException, Query

# load model
MODEL_PATH = "models/xgb_agrimonia_daily.joblib"
model = joblib.load(MODEL_PATH)

# load & preprocess history
RAW_CSV = "data/agrimonia_daily.csv"
raw = pd.read_csv(RAW_CSV, parse_dates=["date"])
raw = raw.sort_values("date").set_index("date")

# feature‐engineering
df = raw.copy()
df["dayofyear"] = df.index.dayofyear
df["month"]     = df.index.month
df["weekday"]   = df.index.weekday

for lag in (1, 2, 3):
    df[f"pm25_lag{lag}"] = df["pm25"].shift(lag)
df["pm25_roll7"]  = df["pm25"].rolling(7).mean()
df["pm25_roll14"] = df["pm25"].rolling(14).mean()

df = df.dropna()

FEATURE_COLS = [
    "pm10","no2","co","nh3",
    "temp_c","humidity","wind_m_s","precip_mm","press_hPa",
    "dayofyear","month","weekday",
    "pm25_lag1","pm25_lag2","pm25_lag3",
    "pm25_roll7","pm25_roll14",
]
features = df[FEATURE_COLS]

app = FastAPI(
    title="AQ Forecast API",
    description="Given a date, returns predicted PM2.5 via the Agrimonia model.",
)

@app.get("/forecast")
def forecast(
    date: _date = Query(
        ...,
        alias="date",
        description=(
            "Date to forecast (YYYY-MM-DD). "
            f"Valid from {features.index.min().date()} to {features.index.max().date()}."
        )
    )
):
    # convert to pandas Timestamp
    ts = pd.Timestamp(date)

    # check if we have that exact timestamp
    if ts not in features.index:
        raise HTTPException(400, f"No data available for {date}")

    # slice out a 1×N DataFrame
    X = features.loc[[ts]]

    # predict
    try:
        y_pred = model.predict(X)[0]
    except Exception as e:
        raise HTTPException(500, f"Prediction error: {e}")

    return {"date": date.isoformat(), "pm25": float(y_pred)}








 