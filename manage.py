#!/usr/bin/env python

import os
from flask import redirect, request, url_for
from flask_migrate import Migrate
from app import create_app, db
from flask import render_template

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """_summary_
            simple login function
    Returns:
        _type_: _description_
    """
    email = ""
    password = ""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if valid_login(email, password):
            data = {"code": 200, "message": "success"}
            redirect("/dashboard", 200, Response=data)

    else:
        redirect("/login", 302, Response="Invalid login")

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """_summary_
        simple login function
    Returns:
        _type_: _description_
    """
    return render_template('dashboard.html')

def valid_login(username, password):
    if username == 'admin@gmail.com' and password == 'admin':
        redirect("/dashboard", 200, Response="Success")
        return True
    else:
        return False

@app.route('/sign-up', methods=['GET'])
def sign_up():
    return render_template('signup.html', error='Please fill out all fields.')

@app.route('/success')
def success():
    print("Form submitted successfully!")
    # Render the form template if the request method is GET
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run()
