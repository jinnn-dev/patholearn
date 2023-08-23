import os
from pusher import Pusher
from app.schema.dataset import Dataset, DatasetStatus

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


def trigger_ws_dataset_status_changed(dataset: Dataset, old_status: str):
    ws_client.trigger(
        "dataset",
        f"status-changed",
        {
            "id": str(dataset.id),
            "name": dataset.name,
            "new_status": dataset.status,
            "old_status": old_status,
        },
    )
