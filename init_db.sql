-- Table for storing price data
CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    price NUMERIC NOT NULL
);

-- Dead Letter Queue (DLQ) table for failed payloads
CREATE TABLE IF NOT EXISTS dlq (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    payload JSONB NOT NULL,
    error_message TEXT
);

-- Function to auto-notify listeners when a new DLQ row is inserted
CREATE OR REPLACE FUNCTION notify_dlq_channel()
RETURNS TRIGGER AS $$
DECLARE
BEGIN
    PERFORM pg_notify('dlq_channel', row_to_json(NEW)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the notify function on insert into DLQ table
DROP TRIGGER IF EXISTS dlq_notify_trigger ON dlq;

CREATE TRIGGER dlq_notify_trigger
AFTER INSERT ON dlq
FOR EACH ROW
EXECUTE FUNCTION notify_dlq_channel();