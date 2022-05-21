import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:8000')
# sio.wait()
while True:
    print("Sending message")
    sio.emit('my_message', 'DAS IST EINE NACHRICHT')
    time.sleep(1)
