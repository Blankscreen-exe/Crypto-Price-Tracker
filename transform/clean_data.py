
from datetime import datetime


def clean_price_payload(payload: dict):
    """
    Validates and formats the extracted payload.
    Ensures required fields exist and types are correct.
    """
    if "timestamp" not in payload or "price" not in payload:
        raise KeyError("Payload missing 'timestamp' or 'price' keys.")

    # Convert timestamp to ISO format if needed
    try:
        if isinstance(payload["timestamp"], str):
            timestamp = datetime.fromisoformat(payload["timestamp"])
        else:
            timestamp = payload["timestamp"]
        iso_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        raise ValueError(f"Invalid timestamp format: {e}")

    # Ensure price is a float
    try:
        price = float(payload["price"])
    except Exception as e:
        raise ValueError(f"Invalid price format: {e}")

    return {
        "timestamp": iso_timestamp,
        "price": price
    }
