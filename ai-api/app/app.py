import os
import logging
import sys

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

from app.config.config import Config
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


@app.post("/projects")
async def create_project(
    create_body: dict, s: SessionContainer = Depends(verify_session())
):
    print(create_body)
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


@app.get("/tasks/{task_id}")
async def get_task(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task(task_id)


@app.get("/tasks/{task_id}/log")
async def get_task_log(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task_log(task_id)


@app.get("/tasks/{task_id}/metrics")
async def get_task_log(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task_metrics(task_id)


@app.post
@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/ping")
def ping():
    return {"Status": "Ok"}