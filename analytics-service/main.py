from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from clickhouse_connect import get_client
import os

app = FastAPI()

# Load ClickHouse credentials from environment variables
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 8123))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "myuser")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "mypass")

# Initialize ClickHouse client
client = get_client(
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_PORT,
    username=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD
)

# Pydantic model for incoming analytics data
class AnalyticsEvent(BaseModel):
    event_name: str
    user_id: str
    timestamp: datetime

@app.post("/analytics")
async def add_analytics(event: AnalyticsEvent):
    try:
        # Insert into ClickHouse
        client.insert(
            "analytics",
            [[event.event_name, event.user_id, event.timestamp]],
            column_names=["event_name", "user_id", "timestamp"]
        )
        return {"message": "Analytics data inserted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics():
    try:
        result = client.query("SELECT * FROM analytics ORDER BY timestamp DESC LIMIT 100")
        return result.result_rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






