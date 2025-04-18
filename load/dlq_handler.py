from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import json

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def handle_dlq(payload, error_message):
    """
    Insert a failed payload into the DLQ table and send a NOTIFY event.
    """
    try:
        payload_json = json.dumps(payload)

        with engine.begin() as conn:
            # Insert into DLQ table
            conn.execute(
                text("""
                    INSERT INTO dlq (timestamp, payload, error_message)
                    VALUES (CURRENT_TIMESTAMP, :payload, :error_message)
                """),
                {"payload": payload_json, "error_message": error_message}
            )

            # Notify listeners (e.g., listener.py) via pg_notify
            conn.execute(
                text("NOTIFY dlq_channel, :payload"),
                {"payload": payload_json}
            )

        print("⚠️ DLQ entry inserted and notification sent.")

    except Exception as e:
        print("❌ Failed to insert into DLQ:", str(e))