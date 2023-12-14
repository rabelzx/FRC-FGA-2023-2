from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Dicionário para armazenar informações sobre os temas
themes = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    theme = data['theme']
    join_room(theme)

    if theme not in themes:
        themes[theme] = {'offer': None, 'answer': None, 'candidates': []}

    emit('theme_joined', theme)

@socketio.on('offer')
def handle_offer(data):
    theme = data['theme']
    themes[theme]['offer'] = data['offer']
    emit('offer_received', data, room=theme, include_self=False)

@socketio.on('answer')
def handle_answer(data):
    theme = data['theme']
    themes[theme]['answer'] = data['answer']
    emit('answer_received', data, room=theme, include_self=False)

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    theme = data['theme']
    themes[theme]['candidates'].append(data['candidate'])
    emit('ice_candidate_received', data, room=theme, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)
