# wildfire-aq-platform

# Wildfire AQ Forecast Platform

**Predict daily PM2.5 concentrations in Lombardy, Italy using historical air-quality, weather, and fire-detection data.**

---

## Project Overview

This project ingests, stores, processes, models, and serves air-quality forecasts via a REST API. Key components:

1. **Ingest**  
   - **Air Pollution data** (AGRIMONIA)
   - **Fire detections** (VIIRS/FIRMS)  

2. **Store**  
   - PostgreSQL + TimescaleDB for time-series data  

3. **Process**  
   - Pandas/SQL to join by date and compute lag/rolling features  

4. **Model**  
   - XGBoost regressor on daily aggregated data (Agrimonia)  
   - Achieves R² ≥ 0.90 

5. **API**  
   - FastAPI service exposing `/forecast?date=YYYY-MM-DD`  

6. **Deploy**  
   - Dockerized containers for API and DB  
   - `docker-compose.yml` for local orchestration  

---

## Repository Structure
```text
.
├── 00-timescaledb.sql        # TimescaleDB extension setup
├── 01-create-tables.sql      # DB table definitions
├── 02-load-agrimonia.sql     # Agrimonia load script (SQL)
├── api.py                    # FastAPI application
├── Dockerfile                # Builds the API container
├── docker-compose.yml        # Orchestrates API + TimescaleDB
├── data/
│   ├── agrimonia_daily.csv   # Final daily dataset
│   └── ...                   # Raw & intermediate CSVs
├── db/
│   └── init.sql              # DB schema & hypertable setup
├── load_agrimonia.py         # Script to load Agrimonia CSV into Postgres/Timescale
├── load_fires.py             # Script to load fire counts into Postgres/Timescale
├── models/                   # Trained model files (.joblib, etc.)
├── notebooks/                # Ingestion, processing, modeling notebooks
├── requirements.txt          # Python dependencies
├── venv/                     # Local virtual environment
└── README.md                 # <-- You are here

```

## Local Setup

### Prerequisites

- Docker & Docker Compose  
- Git  

### 1. Clone & Build

```bash:
git clone https://github.com/your-username/wildfire-aq-platform.git
cd wildfire-aq-platform
```

### 2. Launch
```bash:
docker-compose up --build -d
```
This will start two containers: db: PostgreSQL with TimescaleDB extension, api: FastAPI server at http://localhost:8000

### 3. Load Data
```bash:
python load_agrimonia.py # Load daily air-quality data

python load_fires.py # Load fire-counts time series
```

### 4. Verify Results
```bash:
# Check hypertables
psql postgresql://postgres:postgres@localhost:5432/aq \
  -c "\dt"

# Test API
curl "http://localhost:8000/forecast?date=2017-03-15"
```

### Usage
Forecast endpoint(date must be in span of dataset, 2017-2021): 
```bash:
GET /forecast?date=YYYY-MM-DD
```
Sample Response:
```json:
{
  "date": "2017-03-15",
  "pm25": 46.47
}
```

### Modeling
- Modeling Features: day-of-year, lags (1,2,3,7 days), rolling means, meteorology, fire counts
- Model: XGBoost regressor
- Performance: Test RMSE ≈ 2.7, Test R² ≈ 0.95
- See notebooks/model_agrimonia.ipynb for full training & evaluation.

### Docker
- Dockerfile builds API image
- docker-compose.yml starts both API and TimescaleDB
- To rebuild after changes:
```bash:
docker-compose up --build -d
```






