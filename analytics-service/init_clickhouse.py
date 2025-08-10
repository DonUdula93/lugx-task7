from clickhouse_connect import get_client
import os

client = get_client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
    username=os.getenv("CLICKHOUSE_USER", "myuser"),
    password=os.getenv("CLICKHOUSE_PASSWORD", "mypass")
)

client.command("""
CREATE TABLE IF NOT EXISTS analytics (
    event_name String,
    user_id String,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY timestamp
""")

print("✅ Table 'analytics' created successfully or already exists.")

