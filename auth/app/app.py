import os
from typing import Dict

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from supertokens_python import init, get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.usermetadata.asyncio import (
    update_user_metadata,
)

import sentry_sdk
import httpx
import app.config as config

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
        response = client.get("http://supertokens:3567")
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


app = CORSMiddleware(
    app=app,
    allow_origins=[config.app_info.website_domain],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)
