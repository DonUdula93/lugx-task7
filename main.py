from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import uuid

# NEW: Prometheus instrumentation
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

app = FastAPI()

# Allow frontend requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for frontend
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Expose Prometheus /metrics (works without extra config)
Instrumentator().instrument(app).expose(app)

# Custom metric: total analytics events by type
analytics_events_total = Counter(
    "analytics_events_total",
    "Total analytics events received",
    ["event_type"]
)

# Serve index.html
# @app.get("/")
# async def get_index():
#    return FileResponse("static/index.html")

# Pydantic model for incoming analytics data
class AnalyticsEvent(BaseModel):
    session_id: str
    event_type: str
    page_url: str
    timestamp: datetime
    element_id: str | None = None
    scroll_depth: int | None = None
    time_on_page: float | None = None

# Simulated /track endpoint
@app.post("/track")
async def track_event(event: AnalyticsEvent):
    # increment metric
    analytics_events_total.labels(event_type=event.event_type).inc()

    print("\n Simulated Analytics Event Received:")
    print(f"Event ID: {uuid.uuid4()}")
    print(f"Session: {event.session_id}")
    print(f"Type: {event.event_type}")
    print(f"Page: {event.page_url}")
    print(f"Element: {event.element_id}")
    print(f"Scroll Depth: {event.scroll_depth}")
    print(f"Time on Page: {event.time_on_page}")
    print(f"Timestamp: {event.timestamp}")
    return {"status": "success", "message": "Simulated analytics recorded"}


