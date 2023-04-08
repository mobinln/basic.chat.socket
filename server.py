from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*",)

active_users = []
rooms = {}
messages = []


@app.route('/')
def index():
    return "Server is running"


@socketio.on("connect")
def handle_connect(data):
    print(data)


@socketio.on("ping")
def handle_ping(data):
    body = {}
    body.update(data)
    body.update({"msg": "pong"})
    body.update({"users": active_users, "rooms": rooms})
    emit('pong', body)


@socketio.on('login')
def handle_login(data):
    if "body" in data and not any(d["username"] == data["body"] for d in active_users):
        user = {"username": data["body"], "socketId": request.sid}
        active_users.append(user)
        emit('login', user)
    elif "body" in data and any(d["username"] == data["body"] for d in active_users):
        emit('login', "username already in use")
    else:
        emit('login', "please provide a username")


@socketio.on('join')
def handle_join(data):
    if "body" in data and "room_name" in data["body"]:
        room_name = data["body"]["room_name"]
        user_id = request.sid
        user = next(
            (item for item in active_users if item["socketId"] == user_id), None)

        if room_name not in rooms:
            join_room(room_name)
            rooms.update({"name": room_name, "users": [user]})
            msg = f'{user["username"]} has joined the room {room_name}'

            send('join', msg, to=room_name)
        elif room_name in rooms:
            room_name = data["body"]["room_name"]
            users_updated = rooms[room_name]["users"].append(user)
            msg = f'{user["username"]} has joined the room {room_name}'

            rooms.update({"name": room_name, "users": users_updated})
            send('join', msg, to=room_name)
    elif "body" in data and not "room_name":
        emit('join', "Please enter a room name")


@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('leave_message', f'{username} has left the room', room=room)


@socketio.on('send_message')
def handle_send_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    emit('receive_message', f'{username}: {message}', room=room)


if __name__ == '__main__':
    socketio.run(app, port=5000)
