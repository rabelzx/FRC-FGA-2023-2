from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app)

socketio = SocketIO(app, cors_allowed_origins="*")

# Dicionário para armazenar informações sobre as salas
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)

    if room not in rooms:
        rooms[room] = {'offer': None, 'answer': None, 'candidates': []}

    emit('room_joined', room)

@socketio.on('offer')
def handle_offer(data):
    room = data['room']
    rooms[room]['offer'] = data['offer']
    emit('offer_received', data, room=room, include_self=False)

@socketio.on('answer')
def handle_answer(data):
    room = data['room']
    rooms[room]['answer'] = data['answer']
    emit('answer_received', data, room=room, include_self=False)

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    room = data['room']
    rooms[room]['candidates'].append(data['candidate'])
    emit('ice_candidate_received', data, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)

socketio = SocketIO(app, cors_allowed_origins="*", reconnection=True, reconnection_attempts=3)

