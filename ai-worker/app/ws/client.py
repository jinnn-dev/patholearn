import os
from pusher import Pusher

ws_client = Pusher(
    app_id=os.environ.get("WEBSOCKET_APP_ID"),
    key=os.environ.get("WEBSOCKET_APP_KEY"),
    secret=os.environ.get("WEBSOCKET_APP_SECRET"),
    host="ws",
    port=int(os.environ.get("WEBSOCKET_PORT"))
    if "WEBSOCKET_PORT" in os.environ
    else None,
    ssl=False if os.environ.get("WEBSOCKET_SSL") == "False" else True,
)
