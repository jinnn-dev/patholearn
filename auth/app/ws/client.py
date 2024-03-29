import os
from pusher import Pusher

ws_client = Pusher(
    app_id=os.environ.get("WEBSOCKET_APP_ID"),
    key=os.environ.get("WEBSOCKET_APP_KEY"),
    secret=os.environ.get("WEBSOCKET_APP_SECRET"),
    host=os.environ.get("WEBSOCKET_HOST"),
    port=(
        None
        if "WEBSOCKET_PORT" not in os.environ or os.environ.get("WEBSOCKET_PORT") == ""
        else int(os.environ.get("WEBSOCKET_PORT"))
    ),
    ssl=False if os.environ.get("WEBSOCKET_SSL") == "False" else True,
)
