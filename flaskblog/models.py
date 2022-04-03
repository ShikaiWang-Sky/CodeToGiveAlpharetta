from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin

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

    def check_duplicates(self):
        if int(self.mentor_id) == int(other.mentor_id):
            if str(self.start) == str(other.start):
                return True
        else:
            return False
        pass
    # 'members' backref from User
   

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    # mentor, mentee, admin
    account_type = db.Column(db.String(20), nullable=False)

    interests = db.Column(db.String())
    languages = db.Column(db.String())

    # if User is a mentee, stores mentor
    mentor_id = db.Column(db.Integer)

    # storing mentees id in a space seperated string for now
    # Ex:
    # 1 4 20
    mentees_id = db.Column(db.String())

    # Connecting Users and Meetings with association table
    meetings = db.relationship('Meeting', secondary=user_meeting, backref='members')