from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os
import sys
import time

app = FastAPI()

# -----------------------
# ------------------------
APP_ENV = os.getenv("APP_ENV", "dev")
REQUIRED_TOKEN = os.getenv("API_TOKEN")

if REQUIRED_TOKEN is None:
    print("API_TOKEN is missing. Exit.", file=sys.stderr)
    sys.exit(1)

# ------------------------
# Prometheus metrics
# ------------------------
REQUEST_COUNT = Counter("http_requests_total","Total HTTP requests",["method","endpoint"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds","Request latency",["endpoint"])

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start

    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)

    return response

# ------------------------
# ------------------------
@app.get("/")
def root():
    return {"message": "Health API running", "env":APP_ENV}

@app.get("/health")
def health():
    return {"status":"healthy","service":"health-api-demo2"}

@app.get("/crash")
def crash():
    os._exit(1)

# ------------------------
# metrics endpoint
# ------------------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

