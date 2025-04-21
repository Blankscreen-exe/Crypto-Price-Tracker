import psycopg2
import select
import json
from sqlalchemy import text

from config import config


def insert_into_dlq(payload: dict, error_message: str):
    with config.conf.ENGINE.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO dlq (timestamp, payload, error_message)
                VALUES (CURRENT_TIMESTAMP, :payload, :error_message)
            """),
            {"payload": json.dumps(payload), "error_message": error_message}
        )


def process_failed_event(payload: dict):
    # Custom retry logic goes here — for now, just print
    print(f"Retrying payload: {payload}")
    # You can reprocess here, or move to archive, etc.


def listen_for_dlq():
    conn = psycopg2.connect(config.conf.DB_URL)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    print("🔁 Listening for DLQ NOTIFY events on channel 'dlq_channel'...")
    cur.execute("LISTEN dlq_channel;")

    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            continue  # Timeout passed without activity
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            try:
                payload = json.loads(notify.payload)
                process_failed_event(payload)
            except Exception as e:
                insert_into_dlq(payload=notify.payload, error_message=str(e))
                print("❌ Failed to process DLQ event:", str(e))


if __name__ == "__main__":
    listen_for_dlq()
