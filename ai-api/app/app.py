import os
import logging
import sys
import time
import uuid
import random


from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

import sentry_sdk
from supertokens_python import (
    init,
    get_all_cors_headers,
    SupertokensConfig,
    InputAppInfo,
)
from supertokens_python.recipe import (
    session,
    usermetadata,
)
from supertokens_python.recipe.session import SessionContainer
from app.utils.session import check_session

from supertokens_python.recipe.usermetadata.asyncio import get_user_metadata
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper
from app.router.api_router import api_router
from app.ws.client import ws_client
from app.database.database import client, test_collection

init(
    supertokens_config=SupertokensConfig(
        connection_uri=os.environ.get("SUPERTOKENS_DOMAIN", "http://supertokens:3567")
    ),
    app_info=InputAppInfo(
        app_name="AI Authentication",
        api_domain=os.environ.get("API_DOMAIN", "http://api:3001"),
        website_domain=os.environ.get("WEBSITE_DOMAIN", "http://localhost:5174"),
    ),
    framework="fastapi",
    mode="asgi",
    recipe_list=[
        session.init(
            cookie_domain=os.environ.get("COOKIE_DOMAIN", ".localhost"),
            cookie_secure=True,
            anti_csrf=os.environ.get("ANTI_CSRF", "VIA_TOKEN"),
            session_expired_status_code=401,
        ),
        usermetadata.init(),
    ],
)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

app = FastAPI()
app.include_router(api_router)
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
    allow_headers=["*"] + get_all_cors_headers(),
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/")
async def root():
    start_time = time.time()
    result = []
    async for element in test_collection.find():
        result.append(element)
    print(result)
    print((time.time() - start_time) * 1000)
    return {"Hello": "World"}


@app.get("/insert")
async def insert():
    test = await test_collection.insert_one({"test": "test"})
    new_test = await test_collection.find_one({"_id": test.inserted_id})
    return {"test": new_test["test"]}


@app.get("/ping")
async def ping():
    return "Ok"


@app.get("/ping/clearml")
async def ping_clearml():
    return clearml_wrapper.ping()


@app.post("/auth")
async def ws_login(body: dict, s: SessionContainer = Depends(check_session())):
    channel_name: str = body["channel_name"]

    user_id = s.get_user_id()
    metadataResult = await get_user_metadata(user_id)

    socket_user_id = str(uuid.uuid4())

    if "private-" in channel_name:
        auth = ws_client.authenticate(
            channel=channel_name,
            socket_id=body["socket_id"],
        )
    else:
        auth = ws_client.authenticate(
            channel=channel_name,
            socket_id=body["socket_id"],
            custom_data={
                "user_id": socket_user_id,
                "user_info": {
                    "id": user_id,
                    "color": "#"
                    + "".join([random.choice("0123456789ABCDEF") for j in range(6)]),
                    **(metadataResult.metadata),
                },
            },
        )
    return auth


@app.get("/sessioninfo")
async def secure_api(
    s: SessionContainer = Depends(check_session()),
):
    return {
        "sessionHandle": s.get_handle(),
        "userId": s.get_user_id(),
        "accessTokenPayload": s.get_access_token_payload(),
    }


@app.get("/datasets")
async def login(s: SessionContainer = Depends(check_session())):
    return clearml_wrapper.get_datasets()


@app.get("/datasets/{dataset_id}/images")
async def get_dataset_images(
    dataset_id: str, _: SessionContainer = Depends(check_session())
):
    return clearml_wrapper.get_datatset_debug_images(dataset_id)


@app.get("/datasets/{dataset_project_id}")
async def get_specific_dataset(
    dataset_project_id: str, s: SessionContainer = Depends(check_session())
):
    return clearml_wrapper.get_specific_dataset(dataset_project_id)


@app.post("/projects")
async def create_project(
    create_body: dict, s: SessionContainer = Depends(check_session())
):
    return clearml_wrapper.create_project(
        project_name=create_body["project_name"], description=create_body["description"]
    )


@app.get("/projects")
async def get_projects(s: SessionContainer = Depends(check_session())):
    return clearml_wrapper.get_projects()


@app.get("/projects/{project_id}")
async def get_project(project_id: str, _: SessionContainer = Depends(check_session())):
    return clearml_wrapper.get_project(project_id)


@app.get("/projects/{project_id}/tasks")
async def get_tasks_to_projects(
    project_id: str, s: SessionContainer = Depends(check_session())
):
    return clearml_wrapper.get_tasks_to_project(project_id)


@app.post("/tasks")
async def create_task(data: dict, _: SessionContainer = Depends(check_session())):
    return clearml_wrapper.create_task_and_enque(data)


@app.get("/tasks/{task_id}")
async def get_task(task_id: str, _: SessionContainer = Depends(check_session())):
    return clearml_wrapper.get_task(task_id)


@app.get("/tasks/{task_id}/log")
async def get_task_log(task_id: str, _: SessionContainer = Depends(check_session())):
    return clearml_wrapper.get_task_log(task_id)


@app.get("/tasks/{task_id}/metrics")
async def get_task_log(task_id: str, _: SessionContainer = Depends(check_session())):
    return clearml_wrapper.get_task_metrics(task_id)


@app.post
@app.get("/")
def root():
    return {"Hello": "World"}
