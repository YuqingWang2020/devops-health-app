from fastapi import FastAPI
import os
import sys

app = FastAPI()

APP_ENV = os.getenv("APP_ENV", "dev")
REQUIRED_TOKEN = os.getenv("API_TOKEN")

if REQUIRED_TOKEN is None:
    print("API_TOKEN is missing. Exit.", file=sys.stderr)
    sys.exit(1)

@app.get("/")
def root():
    return {"message": "Health API running", "env":APP_ENV}

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.get("/crash")
def crash():
    os._exit(1)
