from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.utils.logger import logger
from app.utils.minio_client import MinioClient, minio_client

import sentry_sdk

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8001",
    "http://patholearn.de",
    "https://dev.patholearn.de",
]

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.SENTRY_ENVIRONMENT,
    traces_sample_rate=1.0,
)

app.add_middleware(GZipMiddleware, minimum_size=500)

minio_client.create_bucket(MinioClient.hint_bucket)
minio_client.create_bucket(MinioClient.task_bucket)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Hello": "World"}


app.include_router(api_router, prefix=settings.API_STR)
