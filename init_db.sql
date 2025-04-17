CREATE TABLE crypto_prices (
    timestamp TIMESTAMP,
    price FLOAT,
    coin TEXT,
    price_7d_avg FLOAT,
    pct_change FLOAT
);

CREATE TABLE dlq_queue (
    id SERIAL PRIMARY KEY,
    stage TEXT,
    error TEXT,
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT now()
);

-- Trigger to notify Python when a DLQ entry is added
CREATE OR REPLACE FUNCTION notify_dlq() RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('dlq_channel', row_to_json(NEW)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER dlq_notify_trigger
AFTER INSERT ON dlq_queue
FOR EACH ROW EXECUTE FUNCTION notify_dlq();