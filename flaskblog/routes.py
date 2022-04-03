import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session
from flaskblog import app, db, bcrypt
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             ResetPasswordForm)
from flaskblog.models import User, Meeting
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import json
from loguru import logger


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# Registration for mentees
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password,
            account_type='mentee',
            interests=str(form.interests.data),
            languages=str(form.languages.data)
        )

        db.session.add(user)
        db.session.commit()
        print(f"Registered new Mentee! {form.first_name.data} {form.last_name.data}")

        # CONNECT WITH DATABASE

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Login for both mentees/mentors
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  # Set cookies to login
            return redirect(url_for('home'))  # Return redirect to home
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# LOGIN REQUIRED ROUTES

@app.route("/home")
@login_required
def home():
    if current_user.account_type == 'mentor':
        mentees = User.query.filter_by(account_type='mentee').all()
        return render_template("mentor-home.html", title="Home", mentees=mentees, current_user=current_user)

    elif current_user.account_type == 'mentee':
        mentors = User.query.filter_by(account_type='mentor').all()
        return render_template("mentee-home.html", title="Home", mentors=mentors, current_user=current_user)

    elif current_user.account_type == 'admin':
        mentees = User.query.filter_by(account_type='mentee').all()
        mentors = User.query.filter_by(account_type='mentor').all()
        return render_template("admin-home.html", title="Home", mentees=mentees, mentors=mentors)
    else:
        # If an user somehow is not one of the three account_types
        flash("An error occured", "danger")
        return redirect(url_for('logout'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        print("here")
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data

        current_user.interests = str(form.interests.data)
        current_user.languages = str(form.languages.data)

        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # current_user.password=hashed_password

        # user = User.query.filter_by(id=current_user.id)
        # setattr(user, 'first_name', form.first_name.data)

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.interests.data = current_user.interests
        form.languages.data = current_user.languages

    else:
        flash('Error while submitting form.', 'danger')

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)


# TODO: Modify reset_password
@app.route("/reset_token", methods=['GET', 'POST'])
@login_required
def reset_request():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        updated_user = User.query.filter_by(email=current_user.email).first()
        updated_user.password = new_password
        db.session.commit()

        flash('You have successfully change your password', 'info')
        # return redirect(url_for('home'))
    return render_template('reset_token.html', title='resetPassword', form=form)





# For mentors to edit their schedule
@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if current_user.account_type == 'mentor':
        if request.method == 'POST':
            data = request.form['data']
            data = json.loads(data)

            for d in data:
                m = Meeting(
                    mentor_id=current_user.id,
                    start=d['start'],
                    end=d['end'],
                    title=d['title'],
                )
                db.session.add(m)            
            db.session.commit()


        return render_template("schedule.html", meetings=current_user.meetings)
    else:
        flash("An error occured", 'warning')
        return redirect(url_for('home'))


# For mentees to view mentor's schedule
@app.route('/schedule/<id>', methods=['GET', 'POST'])
@login_required
def mentor_schedule(id):
    mentor_id = int(id)
    if current_user.account_type == 'mentee':
        return render_template("schedule.html")


# ADMIN STUFF

@app.route('/manage', methods=['GET'])
@login_required
def manage():
    if current_user.account_type == 'admin':
        mentees = Mentee.query.all()
        mentors = Mentor.query.all()
        return render_template("manage.html", title='Admin Portal', mentees=mentees, mentors=mentors)
    else:
        redirect(url_for('index'))


# TODO: add feature for mentee to recommend mentor: with two type: same interest and same language
@app.route('/recommend', methods=['POST', 'GET'])
@login_required
def recommend():
    if current_user.account_type != 'mentee':
        logger.debug(current_user.account_type)
        return 'error'
    interests, languages = json.loads(current_user.interests), json.loads(current_user.languages)
    # logger.debug(f'interest: {interests[0]}')
    # logger.debug(f'language: {languages[0]}')
    mentors = User.query.filter_by(account_type='mentor').all()
    same_interest, same_language = [], []
    for mentor in mentors:
        mentor_interests = json.loads(mentor.interests)
        mentor_languages = json.loads(mentor.languages)
        for interest in interests:
            if interest in mentor_interests:
                same_interest.append(mentor.id)
                break
        for language in languages:
            if language in mentor_languages:
                same_language.append(mentor.id)
                break

    logger.debug(f'same_interest: {same_interest}')
    logger.debug(f'same_language: {same_language}')
    return 'finish'
