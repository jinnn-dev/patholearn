from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.utils.minio_client import MinioClient, minio_client

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8001",
    "http://patholearn.de",
    "https://dev.patholearn.de",
]


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
