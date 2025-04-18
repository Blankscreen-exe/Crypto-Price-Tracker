from sqlalchemy import create_engine, text
import json
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def reprocess_entry(entry_id):
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT payload FROM dlq WHERE id = :id"),
            {"id": entry_id}
        ).fetchone()

        if not result:
            print(f"❌ No DLQ entry found with ID {entry_id}")
            return

        try:
            if isinstance(result.payload, dict):
                payload = result.payload
            else:
                payload = json.loads(result.payload)
            print(f"🔁 Reprocessing entry {entry_id}: {payload}")

            # Dummy retry logic — replace with your own:
            # e.g., re-insert into ETL queue or call processing function
            if "price" in payload:
                print("✅ Payload looks valid. Consider reinserting into processing pipeline.")

            # Optionally delete after successful reprocess
            conn.execute(
                text("DELETE FROM dlq WHERE id = :id"),
                {"id": entry_id}
            )
            print(f"✅ DLQ entry {entry_id} removed after successful retry.")

        except Exception as e:
            print(f"❌ Failed to reprocess entry {entry_id}: {str(e)}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python reprocessor.py <DLQ_ENTRY_ID>")
    else:
        reprocess_entry(int(sys.argv[1]))
