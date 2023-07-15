import os
from pusher import Pusher
from typing import Any

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


def trigger_ws_task_event(task_id: str, event_name: str, data: Any):
    ws_client.trigger(f"presence-task-{task_id}", event_name, data)


def trigger_ws_task_status_changed(task_id: str, old_status: str, new_status: str):
    trigger_ws_task_event(
        task_id, "training-status-changed", {"old": old_status, "new": new_status}
    )
