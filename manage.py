#!/usr/bin/env python

import json
import os
from flask import request, jsonify, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import openai
from datetime import datetime, timedelta
from app import create_app, db
from models import User, Routine, Feedback
from chatbot import get_user_data_conversation
from daily_engagement import generate_routine_with_ai, extract_first_task,\
        get_next_task

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)

def log_the_user_in(username):
    return f'Hello, {username}!'

@app.route('/')
def index():
    return render_template('index.html')

# Registration Route
@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # print(request)
        # data = request.form.deepcopy()
        # # print(request.form)
        # with open("Output1.txt", "a") as f:
        #     f.write(json.dumps(data) + "\n")
        
        username = request.form.get('username')
        email = request.form.get('email')
        passwd = request.form.get('password')
        print(f"{username}  pass {email}")
        if not username or not email or not passwd:
            return jsonify({'message': 'Missing fields'}), 400
        if User.query.filter_by(username=username).first() or \
                User.query.filter_by(email=email).first():
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # data = request.get_json()
        email = request.form.get('email')
        passwd = request.form.get('password')
        if not email or not passwd:
            return jsonify({'message': 'Missing fields'}), 400
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.passwd_hash, passwd):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('signin.html')
    return render_template('signin.html')

# Logout Route
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Onboarding Route
@app.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    if request.method == 'POST':
        user_input = request.get_json()['user_input']  # User input during onboarding conversation
        conversation_response = get_user_data_conversation(user_input)  # Chatbot conversation handler

        # Once we reach the point of generating a routine
        if 'generate your personalized routine' in conversation_response:
            routine_text = generate_routine_with_ai(user_input)

            new_routine = Routine(
                user_id=current_user.id,
                full_routine=routine_text,
                current_task=extract_first_task(routine_text),
                progress=0,  # Track the number of completed tasks
                last_task_date=datetime.utcnow()  # Date of the last task, for daily task reveal
            )
            db.session.add(new_routine)
            db.session.commit()

            return jsonify({'response': "Onboarding complete! Your first task is ready."})

        return jsonify({'response': conversation_response})

    return render_template('onboarding.html')

# Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    routine = Routine.query.filter_by(user_id=current_user.id).first()

    # Redirect to onboarding if no routine exists
    if not routine:
        return redirect(url_for('onboarding'))

    return render_template('dashboard.html', current_task=routine.current_task)

# Next Task Route (Reveal tasks one day at a time)
@app.route('/next_task', methods=['GET'])
@login_required
def next_task():
    routine = Routine.query.filter_by(user_id=current_user.id).first()

    if not routine:
        return jsonify({'message': 'No routine found! Please complete the onboarding.'}), 404

    # Check if one day has passed since the last task was revealed
    if datetime.utcnow() - routine.last_task_date < timedelta(days=1):
        return jsonify({'message': 'Please wait for the next day to unlock a new task.'}), 403

    next_task_text = get_next_task(routine)

    if next_task_text:
        routine.current_task = next_task_text
        routine.progress += 1
        routine.last_task_date = datetime.utcnow()  # Update the date to track task completion
        db.session.commit()

        return jsonify({'next_task': next_task_text})

    return jsonify({'message': 'You have completed all tasks!'}), 200

# Feedback Route
@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        feedback_input = request.form['feedback']  # Assuming feedback is sent via a form

        # Save feedback to the database
        new_feedback = Feedback(
            user_id=current_user.id,
            feedback_text=feedback_input
        )
        db.session.add(new_feedback)
        db.session.commit()

        # Optionally adjust routine based on feedback
        adjust_routine_based_on_feedback(current_user.id, feedback_input)

        return redirect(url_for('dashboard'))

    return render_template('feedback.html')

def adjust_routine_based_on_feedback(user_id, feedback_input):
    routine = Routine.query.filter_by(user_id=user_id).first()

    if 'difficulty' in feedback_input:
        routine.adjustment = 'Routine made easier based on your feedback.'
    elif 'too easy' in feedback_input:
        routine.adjustment = 'Routine made more challenging based on your feedback.'
    else:
        routine.adjustment = 'Routine updated based on your feedback.'

    db.session.commit()
    
if __name__ == '__main__':
    app.run(host='137.184.100.115')
