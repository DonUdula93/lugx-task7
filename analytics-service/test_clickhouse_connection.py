import clickhouse_connect

print("🔄 Starting ClickHouse connection test...")

try:
    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='myuser',
        password='mypass'
    )
    result = client.query("SELECT 1")
    print("✅ Connected! Result:", result.result_rows)
except Exception as e:
    print("❌ Connection failed:", e)

