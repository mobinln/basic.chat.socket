from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send

import utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*",)

active_users = []
rooms = {}


@app.route('/')
def index():
    return "Server is running"


@socketio.on("connect")
def handle_connect(data):
    print(data)


@socketio.on("disconnect")
def handle_disconnect():
    user_id = request.sid
    index = utils.findIndex(active_users, lambda x,
                            y: x["socketId"] == user_id)
    if index != None:
        del active_users[index]
        for room in rooms:
            for index, user in enumerate(room):
                if user["socketId"] == user_id:
                    del room[index]
    print(f"{user_id} disconnected")


@socketio.on("ping")
def handle_ping(data):
    try:
        user_id = request.sid
        user = next(
            (item for item in active_users if item["socketId"] == user_id), None)

        body = {"msg": "pong", "me": user,
                "active_users": active_users, "rooms": rooms}
        send(body)
    except:
        send("error")


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

        join_room(room_name)
        if room_name not in rooms:
            rooms.update({room_name: [user]})
            msg = f'{user["username"]} has joined the room {room_name}'

            send(msg, to=room_name)
        elif room_name in rooms:
            if any(d["username"] == user['username'] for d in rooms[room_name]):
                msg = f'{user["username"]} has already joined the room {room_name}'
                send(msg, to=room_name)
            else:
                room_name = data["body"]["room_name"]
                users_updated = rooms[room_name].append(user)
                msg = f'{user["username"]} has joined the room {room_name}'

                rooms.update({"name": room_name, "users": users_updated})
                send(msg, to=room_name)
    elif "body" in data and "room_name" not in data["body"]:
        emit('join', "Please enter a room name")


@socketio.on('leave')
def handle_leave(data):
    if "body" in data and "room_name" in data["body"]:
        room_name = data["body"]["room_name"]
        user_id = request.sid
        user = next(
            (item for item in active_users if item["socketId"] == user_id), None)

        if room_name in rooms:
            room = rooms[room_name]

            if any(d['username'] == user['username'] for d in room):
                index = utils.findIndex(
                    room, lambda x, y: x['username'] == user['username'])
                leave_room(room_name)
                del room[index]

                emit('leave_message',
                     f'{user["username"]} has left the room', room=room)
            else:
                send("You are not in the room")
        else:
            send("Room not found")
    elif "body" in data and "room_name" not in data["body"]:
        send("Please enter a room name")


@socketio.on('message')
def handle_send_message(data):
    if "body" in data and "room_name" in data["body"] and 'msg' in data["body"]:
        room_name = data["body"]["room_name"]
        user_id = request.sid
        user = next(
            (item for item in active_users if item["socketId"] == user_id), None)
        msg = data['body']['msg']

        if room_name in rooms:
            room = rooms[room_name]

            if any(d['username'] == user['username'] for d in room):
                send(msg, room=room_name)
            else:
                send("You are not in the room")
        else:
            send("Room not found")
    elif "body" in data and "room_name" not in data["body"]:
        send("Please enter room name and msg")


if __name__ == '__main__':
    socketio.run(app, port=5000)
