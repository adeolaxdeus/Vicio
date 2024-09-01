# app/routes.py

from flask import request, jsonify, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from flask import current_app as app

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Registration Route
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        passwd = data.get('password')

        if not username or not email or not passwd:
            return jsonify({'message': 'Missing fields'}), 400

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return jsonify({'message': 'User already exists'}), 400

        new_user = User(
            username=username,
            email=email,
            passwd_hash=generate_password_hash(passwd)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        passwd = data.get('password')

        if not email or not passwd:
            return jsonify({'message': 'Missing fields'}), 400

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
    return render_template('login.html')

# Logout Route
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Protected Route Example
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')
