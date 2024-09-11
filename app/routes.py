#  Routes for handling onboarding, routine generation, and daily task management.

from flask import request, jsonify, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Routine
from .chatbot import get_user_data_conversation
from .daily_engagement import generate_routine_with_ai, extract_first_task, get_next_task
from flask import current_app as app

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Registration Route
@app.route('/signup', methods=['POST'])
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

        if user and check_password_hash(user.passwd_hash, passwd):
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

@app.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    if request.method == 'POST':
        user_input = request.get_json()  # Get user input during conversation
        conversation_response = get_user_data_conversation(user_input)

        if 'generate your personalized routine' in conversation_response:
            routine_text = generate_routine_with_ai(user_input)
            new_routine = Routine(
                user_id=current_user.id,
                full_routine=routine_text,
                current_task=extract_first_task(routine_text)
            )
            db.session.add(new_routine)
            db.session.commit()
            return redirect(url_for('dashboard'))

        return jsonify({'response': conversation_response})

    return render_template('onboarding.html')

@app.route('/dashboard')
@login_required
def dashboard():
    routine = Routine.query.filter_by(user_id=current_user.id).first()
    if not routine:
        return redirect(url_for('onboarding'))

    return render_template('dashboard.html', current_task=routine.current_task)

@app.route('/next_task', methods=['GET'])
@login_required
def next_task():
    routine = Routine.query.filter_by(user_id=current_user.id).first()
    next_task_text = get_next_task(routine)
    if next_task_text:
        routine.current_task = next_task_text
        db.session.commit()
        return jsonify({'next_task': next_task_text})
    return jsonify({'message': 'You have completed all tasks!'}), 200
