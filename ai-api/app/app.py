import os
import logging
import sys

from fastapi import FastAPI
from fastapi_socketio import SocketManager
from starlette.middleware.cors import CORSMiddleware
import sentry_sdk


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


app = FastAPI()

origins = ["http://localhost:5173", "http://localhost:5174"]

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    environment=os.environ.get("SENTRY_ENVIRONMENT", ""),
    traces_sample_rate=1.0,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = SocketManager(app=app, cors_allowed_origins=[], logger=True)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/ping")
def ping():
    return {"Status": "Ok"}
