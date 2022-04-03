from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


# Registration Forms for Mentees
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    languages = SelectMultipleField(u'Programming Language', choices=[
        ('cpp', 'C++'),
        ('py', 'Python'),
        ('java', 'Java'),
        ('html/css', 'HTML/CSS'),
        ('javascript', 'Javascript')
    ])

    interests = SelectMultipleField(u'Interests', choices =[
        ('health', 'Health'),
        ('finance', 'Finance'),
        ('data', 'Data Science'),
        ('backend', 'Backend'),
        ('frontend', 'Frontend')
    ])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


# Login form for mentee/mentor
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    #picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    languages = SelectMultipleField(u'Programming Language', choices=[
        ('cpp', 'C++'),
        ('py', 'Python'),
        ('java', 'Java'),
        ('html/css', 'HTML/CSS'),
        ('javascript', 'Javascript')
    ])
    interests = SelectMultipleField(u'Interests', choices =[
        ('health', 'Health'),
        ('finance', 'Finance'),
        ('data', 'Data Science'),
        ('backend', 'Backend'),
        ('frontend', 'Frontend')
    ])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
                                     
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


# No email setup, commented out for now
# class RequestResetForm(FlaskForm):
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     submit = SubmitField('Request Password Reset')

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is None:
#             raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
