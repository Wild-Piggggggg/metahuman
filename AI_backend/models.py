from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import Enum
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)
    identity = db.Column(Enum('student', 'officer', name='identity_enum'), nullable=True)
    student_profile = db.relationship('StudentProfile', uselist=False, back_populates='user')
    officer_profile = db.relationship('OfficerProfile', uselist=False, back_populates='user')

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Float, nullable=True)  # nullable=True,表示该字段在数据库或数据模型中允许为空（即可以存储 NULL/None 值）。
    user = db.relationship('User', back_populates='student_profile')  # 反向引用

class OfficerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    major = db.Column(db.String(100), nullable=True)
    user = db.relationship('User', back_populates='officer_profile')

class QuestionBank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    officer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    officer = db.relationship('User', backref=db.backref('questions', lazy=True))