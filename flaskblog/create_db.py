#!/usr/bin/env python3

from flask_bcrypt import Bcrypt
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
from flask import Flask


app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Association Table for many-to-many relationship
user_meeting = db.Table('user_meeting',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'))
)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(), nullable=False)
    end = db.Column(db.String(), nullable=False)

    title = db.Column(db.String(), nullable=False)
    mentor_id = db.Column(db.Integer(), nullable=False)
    mentee_id = db.Column(db.Integer())
    # 'members' backref from User
   

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    # mentor, mentee, admin
    account_type = db.Column(db.String(20), nullable=False)

    interests = db.Column(db.String(), default="")
    languages = db.Column(db.String(), default="")

    # if User is a mentee, stores mentor
    mentor_id = db.Column(db.Integer)

    # storing mentees id in a space seperated string for now
    # Ex:
    # 1 4 20
    mentees_id = db.Column(db.String())

    # Connecting Users and Meetings with association table
    meetings = db.relationship('Meeting', secondary=user_meeting, backref='members')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

def init_db():
    db.drop_all()
    db.create_all()

    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')

    admin = User(
        first_name='Andre',
        last_name='Hu',
        email='andre@mail.com',
        password=hashed_password,
        account_type='admin'
    )

    mentee = User(
        first_name='Bob',
        last_name='McDonald',
        email='bob@mail.com',
        password=hashed_password,
        account_type='mentee',
        languages='["py", "java"]',
        interests='["health", "finance"]'
    )

    mentor1 = User(
        first_name='Sal',
        last_name='Khan',
        email='sal@mail.com',
        password=hashed_password,
        account_type='mentor',
        languages='["py", "cpp"]',
        interests='["data", "finance"]'
    )

    mentor2 = User(
        first_name='Albert',
        last_name='Einstein',
        email='albert@mail.com',
        password=hashed_password,
        account_type='mentor',
        languages='["java"]',
        interests='["health"]'
    )

    db.session.add_all([admin, mentee, mentor1, mentor2])
    db.session.commit()
    print("Database created!")

if __name__ == '__main__':
    init_db()
    