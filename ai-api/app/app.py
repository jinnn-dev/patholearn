import os
import logging
import sys
import time

from fastapi import FastAPI, Depends
from fastapi_socketio import SocketManager
from starlette.middleware.cors import CORSMiddleware
import sentry_sdk
from supertokens_python import (
    init,
    get_all_cors_headers,
    SupertokensConfig,
    InputAppInfo,
)
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
import pusher
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper

init(
    supertokens_config=SupertokensConfig(connection_uri="http://supertokens:3567"),
    app_info=InputAppInfo(
        app_name="AI Authentication",
        api_domain="http://api:3001",
        website_domain="http://localhost:5174",
    ),
    framework="fastapi",
    mode="asgi",
    recipe_list=[
        session.init(anti_csrf="NONE"),
    ],
)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

app = FastAPI()

origins = ["http://localhost:5173", "http://localhost:5174"]

ws_client = pusher.Pusher(
    app_id=os.environ.get("WEBSOCKET_APP_ID"),
    key=os.environ.get("WEBSOCKET_APP_KEY"),
    secret=os.environ.get("WEBSOCKET_APP_SECRET"),
    host="ws",
    port=int(os.environ.get("WEBSOCKET_PORT")),
    ssl=False if os.environ.get("WEBSOCKET_SSL") == "False" else True,
)


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

sio = SocketManager(app=app, cors_allowed_origins=[], logger=True)


@app.get("/ping")
async def ping():
    return "Ok"


@app.get("/ping/clearml")
async def ping_clearml():
    return clearml_wrapper.ping()


@app.get("/sessioninfo")
async def secure_api(
    s: SessionContainer = Depends(verify_session()),
):
    return {
        "sessionHandle": s.get_handle(),
        "userId": s.get_user_id(),
        "accessTokenPayload": s.get_access_token_payload(),
    }


@app.get("/datasets")
async def login(s: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_datasets()


@app.get("/datasets/{dataset_id}/images")
async def get_dataset_images(
    dataset_id: str, _: SessionContainer = Depends(verify_session())
):
    return clearml_wrapper.get_datatset_debug_images(dataset_id)


@app.get("/datasets/{dataset_project_id}")
async def get_specific_dataset(
    dataset_project_id: str, s: SessionContainer = Depends(verify_session())
):
    return clearml_wrapper.get_specific_dataset(dataset_project_id)


@app.post("/projects")
async def create_project(
    create_body: dict, s: SessionContainer = Depends(verify_session())
):
    return clearml_wrapper.create_project(
        project_name=create_body["project_name"], description=create_body["description"]
    )


@app.get("/projects")
async def get_projects(s: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_projects()


@app.get("/projects/{project_id}")
async def get_project(project_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_project(project_id)


@app.get("/projects/{project_id}/tasks")
async def get_tasks_to_projects(
    project_id: str, s: SessionContainer = Depends(verify_session())
):
    return clearml_wrapper.get_tasks_to_project(project_id)


@app.post("/tasks")
async def create_task(data: dict, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.create_task_and_enque(data)


@app.get("/tasks/{task_id}")
async def get_task(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task(task_id)


@app.get("/tasks/{task_id}/log")
async def get_task_log(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task_log(task_id)


@app.get("/tasks/{task_id}/metrics")
async def get_task_log(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task_metrics(task_id)


@app.get("/")
def root():
    result = ws_client.trigger("chat-bot", "message", "Das ist eine Nachricht")
    print(
        os.environ.get("WEBSOCKET_APP_ID"),
        os.environ.get("WEBSOCKET_APP_KEY"),
        os.environ.get("WEBSOCKET_APP_SECRET"),
        os.environ.get("WEBSOCKET_HOST"),
        int(os.environ.get("WEBSOCKET_PORT")),
        False if os.environ.get("WEBSOCKET_SSL") == "False" else True,
    )
    return {"Hello": "World"}
