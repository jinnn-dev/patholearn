import sentry_sdk
import socketio
from fastapi import FastAPI, HTTPException
# from sentry_sdk import set_tag
# from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.api.api import api_router
from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import SessionManager
from app.sockets.TaskNamespace import TaskNamespace
from app.utils.minio_client import MinioClient, minio_client

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[])
socketio_app = socketio.ASGIApp(sio)

# sio.register_namespace(TaskNamespace())

app = FastAPI()

app.mount("/ws", socketio_app)

open_rooms = {}


@sio.event
def connect(sid, environ, auth):
    with SessionManager() as db:
        token = auth["token"]
        if token is None:
            raise ConnectionRefusedError("authentication failed")
        try:
            get_current_user(db=db, token=token)
        except HTTPException:
            raise ConnectionRefusedError("authentication failed")


@sio.on('connect', namespace='/task')
async def connect(sid, environ, auth):
    with SessionManager() as db:
        if "token" not in auth:
            raise ConnectionRefusedError("authentication failed")
        token = auth["token"]
        if token is None:
            raise ConnectionRefusedError("authentication failed")
        try:
            user = get_current_user(db=db, token=token)
            print(f"{user.firstname} connected")
            async with sio.session(sid, namespace='/task') as session:
                session['username'] = user.firstname
        except HTTPException:
            raise ConnectionRefusedError("authentication failed")


@sio.on('disconnect', namespace='/task')
async def disconnect(sid):
    async with sio.session(sid, namespace='/task') as session:
        username = session['username']
        print(f"{username} disconnected")

        for key in list(open_rooms.keys()):
            if key in open_rooms:
                open_rooms[key].remove(username)
                if len(open_rooms[key]) == 0:
                    del open_rooms[key]
        print("Open rooms after disconnect", open_rooms)
        await sio.emit('user-left', namespace='/task', data=username)


@sio.on('create_room', namespace='/task')
async def create_room(sid, data):
    base_task_shortname = data["base_task_shortname"]
    task_id = data["task_id"]

    room_id = base_task_shortname + '-' + str(task_id)

    if room_id not in open_rooms.keys():
        open_rooms[room_id] = []
    async with sio.session(sid, namespace='/task') as session:
        print(f"create_room request from {session}")
        open_rooms[room_id].append(session['username'])
        sio.enter_room(sid, room_id, namespace='/task')
        await sio.emit('user-joined', room=room_id, namespace='/task',
                       data={"user": session['username'], "user_list": open_rooms[room_id], "room_id": room_id})

        print("Open rooms after join", open_rooms)


@sio.on('user-indicator-update', namespace='/task')
async def user_indicator_update(sid, room_id, x, y):
    async with sio.session(sid, namespace='/task') as session:
        data = {"user": session['username'], "x": x, "y": y}
        await sio.emit('user-indicator-update', room=room_id, data=data, namespace='/task', skip_sid=sid)


@sio.event
def my_message(sid, data):
    print('message', data, sid)


@sio.event
def disconnect(sid):
    print('disconnect', sid)


# if settings.SENTRY_METRICS:
#     print("Sentry running")
#     sentry_sdk.init(
#         settings.SENTRY_URL,
#         traces_sample_rate=1.0
#     )
#     set_tag("environment", settings.SENTRY_ENVIRONMENT_TAG)

origins = [
    "http://localhost:3000",
    "https://patholearn.de"
]

# if settings.SENTRY_METRICS:
#     try:
#         app.add_middleware(SentryAsgiMiddleware)
#     except Exception:
#         pass

minio_client.create_bucket(MinioClient.hint_bucket)
minio_client.create_bucket(MinioClient.task_bucket)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)


@app.get("/")
def root():
    return {"Hello": "World"}


app.include_router(api_router, prefix=settings.API_STR)
