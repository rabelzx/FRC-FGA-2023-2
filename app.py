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
app.config['MYSQL_PASSWORD'] = 'tigreazul21'
app.config['MYSQL_DB'] = 'videoChatApp'

rooms = {}  # Dictionary to store users and messages in each room
  
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

#rota para logar
@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM usuario WHERE username = % s AND password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'

    return render_template('login.html', msg = msg) 

#rota para deslogar
@app.route('/logout') 
def logout(): 
   session.pop('loggedin', None) 
   session.pop('id', None) 
   session.pop('username', None) 
   return redirect(url_for('login')) 
  
#rota para cadastrar usuário
@app.route('/register', methods =['GET', 'POST']) 
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        chat = request.form['chat']  # Adicionando a captura da opção de chat

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuario WHERE username = %s', (username, ))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'name must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO usuario (username, password, chat, status) VALUES (%s, %s, %s, %s)',
                           (username, password, chat, 'offline'))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)
  
  
@app.route("/index") 
def index(): 
    if 'loggedin' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT id, username, status FROM usuario')  # Inclua o status na consulta
        users = cursor.fetchall()

        # Converter os resultados para um formato JSON
        user_list = [{'id': user['id'], 'name': user['username'], 'status': user['status']} for user in users]
        
        # Filtrar usuários online, offline e ocupados
        online_users = [user for user in user_list if user['status'] == 'online']
        offline_users = [user for user in user_list if user['status'] == 'offline']
        ocupado_users = [user for user in user_list if user['status'] == 'ocupado']

        return render_template("index.html", users=user_list,  online_users=online_users, offline_users=offline_users, ocupado_users=ocupado_users)  
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
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'chat' in request.form and 'status' in request.form:
            username = request.form['username']
            password = request.form['password']
            chat = request.form['chat']
            status = request.form['status']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM usuario WHERE username = % s', (username, ))
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
    session['room'] = 'room1'  # Use a default room
    join_room(session['room'])
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
app.config['MYSQL_PASSWORD'] = 'tigreazul21'
app.config['MYSQL_DB'] = 'videoChatApp'

rooms = {}  # Dictionary to store users and messages in each room
  
  
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
@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM usuario WHERE username = % s AND password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg) 
  
@app.route('/logout') 
def logout(): 
   session.pop('loggedin', None) 
   session.pop('id', None) 
   session.pop('username', None) 
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
    session['room'] = 'room1'  # Use a default room
    join_room(session['room'])
    rooms.setdefault(session['room'], {'users': set(), 'messages': []})
    rooms[session['room']]['users'].add(session['username'])
    emit_users()

@socketio.on('disconnect')
def handle_disconnect():
    room = session.get('room')
    if room:
        leave_room(room)
        rooms[room]['users'].discard(session['id'])
        emit_users()

@socketio.on('message')
def handle_message(data):
    username = session['username']
    message = data['message']
    room = session['room']

    # Print the message in the server terminal
    print(f"Client {username} in Room {room}: {message}")

    # Store the message in the room
    rooms[room]['messages'].append({'username': username, 'message': message})

    # Broadcast the message to all clients in the same room, including the sender
    emit('message', {'message': message, 'username': username}, room=room)
    emit_users()

@socketio.on('join_room')
def handle_join_room(data):
    old_room = session.get('room')
    if old_room:
        leave_room(old_room)
        rooms[old_room]['users'].discard(session['username'])

    session['room'] = data['room']
    join_room(session['room'])
    rooms.setdefault(session['room'], {'users': set(), 'messages': []})
    rooms[session['room']]['users'].add(session['username'])
    emit_users()

def emit_users():
    room_users = rooms[session['room']]['users']
    user_list = [{'id': username, 'name': username} for username in room_users]
    emit('users', {'clients': user_list}, broadcast=True)
  
#chat de vídeo
themes = {}

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

if __name__ == "__main__": 
    criar_tabela()
    socketio.run(app, debug=True)