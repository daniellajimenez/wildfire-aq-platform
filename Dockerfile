FROM python:3.12-slim

# set working dir
WORKDIR /app

# install OS-level deps
RUN apt-get update \
 && apt-get install -y build-essential --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# copy & install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# expose & run
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
