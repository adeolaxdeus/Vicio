from app import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwd_hash = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, \
            onupdate=datetime.utcnow)

    addictions = db.relationship('Addiction', backref='user', lazy=True)
    routines = db.relationship('Routine', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Addiction(db.Model):
    __tablename__ = 'addictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    addiction_type = db.Column(db.String(70), nullable=False)
    addiction_cause = db.Column(db.String(300))
    severity_level = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, \
            onupdate=datetime.utcnow)

    routines = db.relationship('Routine', backref='addiction', lazy=True)

    def __repr__(self):
        return f'<Addiction {self.addiction_type} for User {self.user_id}>'

class Routine(db.Model):
    __tablename__ = 'routines'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    addiction_id = db.Column(db.Integer, db.ForeignKey('addictions.id'), \
            nullable=False)
    routine_description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, \
            onupdate=datetime.utcnow)

    feedbacks = db.relationship('Feedback', backref='routine', lazy=True)

    def __repr__(self):
        return f'<Routine {self.id} for User {self.user_id}>'

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    routinue_id = db.Column(db.Integer, db.ForeignKey('routines.id'), \
            nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    ratings = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Feedback {self.id} for Routine {self.routine_id}>'

