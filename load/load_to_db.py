from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def insert_price(timestamp, price):
    """
    Inserts a single price record into the prices table.
    """
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO prices (timestamp, price)
                VALUES (:timestamp, :price)
            """),
            {"timestamp": timestamp, "price": price}
        )