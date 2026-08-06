from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ---------- DATABASE MODELS ----------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tutorial_name = db.Column(db.String(120), nullable=False)
    percent_complete = db.Column(db.Integer, default=0)

# Sample data (later you can move this to the database)
TUTORIALS = [
    {"id": 1, "title": "Python Basics", "language": "Python", "level": "Beginner"},
    {"id": 2, "title": "JavaScript DOM", "language": "JavaScript", "level": "Beginner"},
    {"id": 3, "title": "Flask Web Apps", "language": "Python", "level": "Intermediate"},
    {"id": 4, "title": "React Fundamentals", "language": "JavaScript", "level": "Intermediate"},
]

PROJECTS = [
    {"id": 1, "title": "To-Do List App", "level": "Beginner", "online": True},
    {"id": 2, "title": "Weather Dashboard", "level": "Intermediate", "online": True},
    {"id": 3, "title": "E-commerce Site", "level": "Advanced", "online": False},
]

# ---------- ROUTES ----------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tutorials')
def tutorials():
    language = request.args.get('language')
    level = request.args.get('level')
    filtered = TUTORIALS
    if language:
        filtered = [t for t in filtered if t['language'] == language]
    if level:
        filtered = [t for t in filtered if t['level'] == level]
    return render_template('tutorials.html', tutorials=filtered)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # In a real app, you'd send an email or save to DB here
        flash('Message sent successfully!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('signup'))

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    progress = Progress.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', progress=progress, username=session.get('username'))

# ---------- INIT DATABASE ----------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
