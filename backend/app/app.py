import sentry_sdk
from fastapi import FastAPI
# from sentry_sdk import set_tag
# from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.utils.minio_client import MinioClient, minio_client

app = FastAPI()

# if settings.SENTRY_METRICS:
#     print("Sentry running")
#     sentry_sdk.init(
#         settings.SENTRY_URL,
#         traces_sample_rate=1.0
#     )
#     set_tag("environment", settings.SENTRY_ENVIRONMENT_TAG)

origins = [
    "http://10.168.2.105:3000",
    "http://localhost:3000",
    "http://localhost:8001"
    "*"
]

app.add_middleware(GZipMiddleware, minimum_size=500)

# if settings.SENTRY_METRICS:
#     try:
#         app.add_middleware(SentryAsgiMiddleware)
#     except Exception:
#         pass

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
