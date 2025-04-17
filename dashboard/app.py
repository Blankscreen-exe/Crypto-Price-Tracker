from flask import Flask, render_template
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


@app.route("/")
def index():
    with engine.connect() as conn:
        query = text("""
            SELECT timestamp, price
            FROM prices
            ORDER BY timestamp DESC
            LIMIT 100
        """)
        df = pd.read_sql(query, conn).sort_values("timestamp")

    # Compute 7-day (or 7-point) moving average
    df["moving_avg"] = df["price"].rolling(window=7).mean().fillna(method="bfill")

    timestamps = df["timestamp"].astype(str).tolist()
    prices = df["price"].tolist()
    moving_avg = df["moving_avg"].tolist()

    return render_template(
        "index.html",
        timestamps=timestamps,
        prices=prices,
        moving_avg=moving_avg
    )


@app.route("/dlq")
def dlq_view():
    with engine.connect() as conn:
        query = text("""
            SELECT id, timestamp, payload, error_message
            FROM dlq
            ORDER BY timestamp DESC
            LIMIT 50
        """)
        results = conn.execute(query).fetchall()

    dlq_entries = [
        {
            "timestamp": row["timestamp"],
            "payload": row["payload"],
            "error_message": row["error_message"]
        }
        for row in results
    ]

    return render_template("dlq.html", dlq_entries=dlq_entries)


if __name__ == "__main__":
    app.run(debug=True)
