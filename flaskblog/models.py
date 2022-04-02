from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin


# How will the backend know if the user is a Mentor or Mentee?
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Association Table for many-to-many relationship
user_meeting = db.Table('user_meeting',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('meeting_id', db.Integer, db.ForeignKey('channel.id'))
)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(DateTime(), nullable=False)
    end = db.Column(DateTime(), nullable=False)
    # 'members' backref from User
   

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
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


    # TODO: setup password reset
    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"






# class Mentor(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(120), nullable=False)
#     last_name = db.Column(db.String(120), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

#     languages = db.Column(db.String())  # 'cpp:python:javascript'
#     # interests = db.Column(db.String())

#     # Mentor can have mentees
#     mentees = db.relationship('Mentee', backref='mentor', lazy=True)
#     meetings = db.relationship('Meeting', backref='mentor_id', lazy=True)


# class Mentee(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(120), nullable=False)
#     last_name = db.Column(db.String(120), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

#     languages = db.Column(db.String())
#     # interests = db.Column(db.String())

#     meetings = db.relationship('Meeting', backref='mentee_id', lazy=True)

    # 'mentor' object connecting to mentor table

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"
