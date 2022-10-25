from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.persistance.minio_wrapper import MinioWrapper

app = FastAPI()

minio_wrapper = MinioWrapper()
minio_wrapper.init_buckets()

origins = [
    "http://localhost:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def test():
    return {"Hello": "World"}


app.include_router(api_router)
