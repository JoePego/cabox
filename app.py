from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Ash:Ash4856@localhost/chatdb'
db = SQLAlchemy(app)
socketio = SocketIO(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

def create_db():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', show_sidebar=True)

# removed for temporary period
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if not username or not password:
#             flash('Please fill out all fields', 'danger')
#             return redirect(url_for('login'))
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             flash('Login successful', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login failed. Check your credentials', 'danger')
#     return render_template('login.html', show_sidebar=False)    

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         if not username or not email or not password:
#             flash('Please fill out all fields', 'danger')
#             return redirect(url_for('signup'))
#         hashed_password = generate_password_hash(password).decode('utf-8')
#         user = User(username=username, email=email, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Signup successful, please log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('signup.html', show_sidebar=False)
        

# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     user = User.query.get(session['user_id'])
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         if not username or not email:
#             flash('Username and email are required', 'danger')
#         else:
#             user.username = username
#             user.email = email
#             if password:
#                 user.password = generate_password_hash(password).decode('utf-8')
#             db.session.commit()
#             flash('Profile updated', 'success')
#     return render_template('profile.html', user=user, show_sidebar=False)

@socketio.on('message')
def handleMessage(msg):
    if 'user_id' in session:
        send(msg, broadcast=True)
    else:
        flash('You must be logged in to send messages', 'danger')

if __name__ == '__main__':
    with app.app_context():
        create_db()
    socketio.run(app, debug=True)
