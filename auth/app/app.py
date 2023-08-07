import os
from typing import Dict
import uuid
import random
import sentry_sdk
import httpx

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from supertokens_python import init, get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.usermetadata.asyncio import (
    update_user_metadata,
)
from supertokens_python.recipe.usermetadata.asyncio import get_user_metadata


import app.config as config
from app.ws.client import ws_client

init(
    supertokens_config=config.supertokens_config,
    app_info=config.app_info,
    framework=config.framework,
    recipe_list=config.recipe_list,
    mode="asgi",
)

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    environment=os.environ.get("SENTRY_ENVIRONMENT", ""),
    traces_sample_rate=1.0,
)

app = FastAPI(title="Patholearn Authentication ")
app.add_middleware(get_middleware())


@app.get("/ping")
async def ping():
    with httpx.Client() as client:
        response = client.get(
            os.environ.get("SUPERTOKENS_DOMAIN", "http://supertokens:3567")
        )
    return "Ok" if response.status_code == 200 else "Error"


@app.get("/sessioninfo")
async def secure_api(s: SessionContainer = Depends(verify_session())):
    return {
        "sessionHandle": s.get_handle(),
        "userId": s.get_user_id(),
        "accessTokenPayload": s.get_access_token_payload(),
    }


@app.put("/user/metadata")
async def set_user_metadata(
    metadata: Dict, s: SessionContainer = Depends(verify_session())
):
    user_id = metadata["user_id"]
    data = metadata["metadata"]
    result = await update_user_metadata(user_id, data)
    return result


@app.post("/ws")
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


app = CORSMiddleware(
    app=app,
    allow_origins=[config.app_info.website_domain],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)
