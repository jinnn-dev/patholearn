import os
import logging
import sys
import time
import uuid
import random

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
from supertokens_python.recipe import session, usermetadata
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.usermetadata.asyncio import get_user_metadata
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper
from app.router.api_router import api_router
from app.ws.client import ws_client
from app.database.database import client, test_collection

init(
    supertokens_config=SupertokensConfig(connection_uri="http://supertokens:3567"),
    app_info=InputAppInfo(
        app_name="AI Authentication",
        api_domain="http://api:3001",
        website_domain="http://localhost:5174",
    ),
    framework="fastapi",
    mode="asgi",
    recipe_list=[session.init(anti_csrf="NONE"), usermetadata.init()],
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

sio = SocketManager(app=app, cors_allowed_origins=[], logger=True)


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
async def ws_login(body: dict, s: SessionContainer = Depends(verify_session())):
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
    s: SessionContainer = Depends(verify_session()),
):
    return {
        "sessionHandle": s.get_handle(),
        "userId": s.get_user_id(),
        "accessTokenPayload": s.get_access_token_payload(),
    }
