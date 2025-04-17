# 📈 Crypto Price Tracker with Real-Time Dead Letter Queue (DLQ)

A production-style ETL pipeline that extracts cryptocurrency price data, 
computes statistics, stores it in a PostgreSQL database, and displays a 
visual dashboard using Flask. The pipeline includes a robust **Dead Letter Queue** 
mechanism powered by PostgreSQL's `LISTEN/NOTIFY` to handle and monitor 
data ingestion failures in real time.

---

## 🚀 Features

- ✅ **ETL pipeline** for Bitcoin price data (CoinGecko API)
- 📊 **Flask dashboard** with real-time charting using Chart.js
- 📉 **7-day moving average** and percent change calculations
- 🧠 **Dead Letter Queue (DLQ)** for graceful error handling
- 🔔 **PostgreSQL-based real-time queue** using `LISTEN/NOTIFY`
- 🛠️ Modular structure (extract/transform/load/dashboard)
- 🧪 Easily extendable for other coins, metrics, or APIs

---

## 🗂️ Project Structure

```
crypto_etl/ 
├── extract/ # CoinGecko API data fetcher
├── transform/ # Data cleaning & enrichment
├── load/ # DB loader + DLQ insertion
├── dlq/ # Real-time listener & optional retry logic
├── dashboard/ # Flask UI for dashboard & DLQ viewer
├── run_pipeline.py # Entrypoint for running ETL
├── init_db.sql # DB schema setup & triggers
├── requirements.txt # Dependencies
└── .env # Environment variables
```

---

## 🔧 Tech Stack

| Layer       | Tools Used                   |
|------------|-------------------------------|
| Language    | Python 3.10+                  |
| Data Source | [CoinGecko API](https://www.coingecko.com/en/api) |
| Database    | PostgreSQL                    |
| Backend     | Flask                         |
| Charts      | Chart.js                      |
| Real-time   | PostgreSQL LISTEN/NOTIFY      |

---

## 🛠️ Setup Instructions

1. Install dependencies

  ```bash
  pip install -r requirements.txt
  ```

2. Set up PostgreSQL. Create a new DB and run the schema:

  ```bash
  psql -U your_user -d your_db -f init_db.sql
  ```

3. Then add your .env file:

  ```env
  DATABASE_URL=postgresql://your_user:your_password@localhost:5432/your_db
  ```

## How To Run

1. Run the real-time DLQ listener

```bash
python dlq/listener.py
```

2. Run the ETL pipeline

```bash
python run_pipeline.py
```

3. Start the dashboard

```bash
python dashboard/app.py
```

4. Open `http://localhost:5000` for the dashboard or go to `http://localhost:5000/dlq` to view DLQ entries

