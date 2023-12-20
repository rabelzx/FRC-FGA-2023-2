from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import MySQLdb.cursors 
import re 
  
  
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")
  
  
app.secret_key = 'your secret key'
  
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'videoChatApp'

rooms = {}
  
  
mysql = MySQL(app) 

def criar_tabela():
    with app.app_context():
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS usuario (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            password VARCHAR(255),
            chat VARCHAR(255),
            status VARCHAR(20) DEFAULT 'offline'
        )
        '''
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(create_table_query)
 
@app.route('/') 
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuario WHERE username = %s AND password = %s', (username, password, ))
        account = cursor.fetchone()
        
        if account:
            # Atualiza o status para "online"
            cursor.execute('UPDATE usuario SET status = %s WHERE id = %s', ('online', account['id']))
            mysql.connection.commit()

            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            get_user_status()
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    
    return render_template('login.html', msg=msg)
  
@app.route('/logout') 
def logout():
    if 'loggedin' in session:
        username_to_emit = session.get('username', None)  # Armazena o valor de 'username'
        
        # Atualiza o status para "offline" ao fazer logout
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE usuario SET status = %s WHERE id = %s', ('offline', session['id']))
        mysql.connection.commit()

        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)

        get_user_status()
    
    return redirect(url_for('login'))
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        chat = request.form['chat']  # Adicionando a captura da opção de chat
        status = 'offline'  # Defina um valor padrão para o status

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuario WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO usuario (username, password, chat, status) VALUES (%s, %s, %s, %s)',
                           (username, password, chat, status))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)

  
  
@app.route("/index") 
def index(): 
    if 'loggedin' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT id, username FROM usuario') 
        users = cursor.fetchall()

        # Converter os resultados para um formato JSON
        user_list = [{'id': user['id'], 'name': user['username']} for user in users]
        print("Users:", user_list)  # Adicione este print para verificar a lista de usuários
        get_user_status()
        return render_template("index.html", users=user_list)  
    return redirect(url_for('login')) 
  
@app.route("/display") 
def display(): 
    if 'loggedin' in session: 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM usuario WHERE id = % s', (session['id'], )) 
        account = cursor.fetchone()     
        return render_template("display.html", account = account) 
    return redirect(url_for('login')) 
  
@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form \
                and 'chat' in request.form and 'status' in request.form:
            username = request.form['username']
            password = request.form['password']
            chat = request.form['chat']
            status = request.form['status']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM usuario WHERE username = %s', (username,))
            account = cursor.fetchone()

            if account:
                if not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'name must contain only characters and numbers !'
                else:
                    cursor.execute(
                        'UPDATE usuario SET username = %s, password = %s, chat = %s, status = %s WHERE id = %s',
                        (username, password, chat, status, session['id']))
                    mysql.connection.commit()
                    msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))


@socketio.on('connect')
def handle_connect():
    session['room'] = 'room0'  # Use a default room
    join_room(session['room'])
    rooms.setdefault(session['room'], {'users': set(), 'messages': []})
    rooms[session['room']]['users'].add(session['username'])
    get_user_status()
    emit_users()

@socketio.on('disconnect')
def handle_disconnect():
    room = session.get('room')
    if room:
        leave_room(room)
        rooms[room]['users'].discard(session['id'])
        get_user_status()
        emit_users()

@socketio.on('message')
def handle_message(data):
    username = session['username']
    message = data['message']
    room = session['room']

    # Print the message in the server terminal
    print(f"Client {username} in Room {room}: {message}")

    # Adicione a mensagem à sala específica
    rooms[room]['messages'].append({'username': username, 'message': message})

    # Broadcast a mensagem para todos na sala
    emit('message', {'message': message, 'username': username, 'room': room}, room=room)
    get_user_status()
    emit_users()

@socketio.on('join_room')
def handle_join_room(data):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE usuario SET status = %s WHERE id = %s', ('ocupado', session['id']))
    mysql.connection.commit()
    old_room = session.get('room')
    if old_room:
        leave_room(old_room)
        rooms[old_room]['users'].discard(session['username'])

    session['room'] = data['room']
    join_room(session['room'])
    rooms.setdefault(session['room'], {'users': set(), 'messages': []})
    rooms[session['room']]['users'].add(session['username'])
    get_user_status()
    emit_users()

def emit_users():
    room_users = rooms[session['room']]['users']
    user_list = [{'id': username, 'name': username} for username in room_users]
    emit('users', {'clients': user_list, 'room': session['room'], 'room_users': list(room_users)}, broadcast=True)

def get_user_status():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT username, status FROM usuario')
    users = cursor.fetchall()
    print("Users from DB:", users)  # Adicione este print
    online_users = [user['username'] for user in users if user['status'] == 'online']
    offline_users = [user['username'] for user in users if user['status'] == 'offline']
    ocupado_users = [user['username'] for user in users if user['status'] == 'ocupado']
    print("Online Users:", online_users)  # Adicione este print
    print("Offline Users:", offline_users)  # Adicione este print
    print("Ocupado:", ocupado_users)
    socketio.emit('update_user_list', {'online_users': online_users, 'offline_users': offline_users, 'ocupado_users': ocupado_users})
  
#chat de vídeo
themes = {}

@socketio.on('join_video')
def handle_join(data):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE usuario SET status = %s WHERE id = %s', ('ocupado', session['id']))
    mysql.connection.commit()
    theme = data['theme']
    join_room(theme)

    if theme not in themes:
        themes[theme] = {'offer': None, 'answer': None, 'candidates': []}
    get_user_status()

    emit('theme_joined', theme)

@socketio.on('leave_video')
def handle_leave(data):
    theme = data['theme']
    leave_room(theme)
    emit('theme_left', theme)

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

if __name__ == "__main__": 
    criar_tabela()
    socketio.run(app, debug=True)
