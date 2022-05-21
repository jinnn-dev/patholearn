import socketio

class TaskNamespace(socketio.AsyncNamespace):

    def __init__(self):
        super().__init__('/task')

    def on_connect(self, sid, environ):
        print(f"User {sid} connected to the task namespace")

    async def on_create_room(self, sid, data):

        print(f"{sid} wants to create room")

    def on_disconnect(self, sid):
        print(f"User {sid} disconnected from task namespace")
# from app.app import sio
#
#
# @sio.on('connect', namespace='/task')
# def connect(sid, environ):
#     print(f"{sid} connected to task namespace")
#
#
# @sio.on('create_room', namespace='/task')
# def create_room(sid, data):
#     print(sid, data)
