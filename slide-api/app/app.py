from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.persistance.minio_wrapper import MinioWrapper

import sentry_sdk
import os

app = FastAPI()

minio_wrapper = MinioWrapper()
minio_wrapper.init_buckets()

origins = ["http://localhost:8000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)


@app.get("/")
def test():
    return {"Hello": "World"}


app.include_router(api_router)
