CREATE DATABASE IF NOT EXISTS receipts;

CREATE TABLE IF NOT EXISTS receipts.checks
(
    id UUID DEFAULT generateUUIDv4(),
    shop_name String,
    total Float64,
    created_at DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (created_at);