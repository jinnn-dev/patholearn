from supertokens_python.recipe.session.framework.fastapi import verify_session

from supertokens_python.recipe.session.exceptions import TryRefreshTokenError
from fastapi import HTTPException


def check_session():
    from fastapi import Request

    async def func(request: Request):
        func = verify_session()

        try:
            session = await func(request)
            return session
        except TryRefreshTokenError as e:
            raise HTTPException(status_code=401, detail="Session expired")

    return func
