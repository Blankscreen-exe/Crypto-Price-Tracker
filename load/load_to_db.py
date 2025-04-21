from sqlalchemy import text

from config import config


def insert_price(timestamp, price):
    """
    Inserts a single price record into the prices table.
    """
    with config.conf.ENGINE.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO prices (timestamp, price)
                VALUES (:timestamp, :price)
            """),
            {"timestamp": timestamp, "price": price}
        )