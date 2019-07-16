from flask import (render_template, Blueprint, redirect, flash, request,
                   url_for, abort)
from flask_login import (current_user, login_user, logout_user,
                         fresh_login_required)
from datetime import datetime, timedelta

import os
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from .. import app, db
from ..models import User, Posts
from .forms import LoginForm, SignUpForm, EditProfileForm
from ..picture_handler import process_image

user = Blueprint('user', __name__)


@user.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@user.route('/', methods=['GET', 'POST'])
def home():
    return render_template("user/user_home.html")


@user.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        form.username.data = current_user.username
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            if form.remember_me.data:
                login_user(user, remember=True, duration=timedelta(days=5))
            login_user(user)
            flash('Successful Login', 'success')
            next_url = request.args.get('next')
            if not next_url or url_parse(next_url).netloc != '':
                return redirect(url_for("user.home"))
            return redirect(next_url)
        else:
            flash('Incorrect Username or Password', 'danger')
            form.username.data = ''
            form.password.data = ''
    return render_template("user/user_login.html", form=form)


@user.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('user.login'))


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully !', 'success')
        return redirect(url_for("user.login"))
    return render_template("user/user_signup.html", form=form,
                           title='App-Sign Up')


# todo : create reset password functionality
@user.route('/reset_password')
def reset_password():
    return "Being prepared"


@user.route("/profile/<uname>")
@fresh_login_required
def profile(uname):
    if uname == current_user.username:
        page_num = request.args.get('page', default=1, type=int)
        user = User.query.filter_by(username=uname).first()
        posts = Posts.query.filter_by(author=user).order_by(
            Posts.creation_date.desc()).paginate(page=page_num, per_page=5)
        return render_template("user/user_profile.html", posts=posts,
                               page_num=page_num)
    else:
        abort(403)


@user.route("/edit_profile/", methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.username = form.username.data
        user.about_me = form.about_me.data
        file = form.profile_picture.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.profile_pic = process_image(filename,
                                             user.username)
        db.session.commit()
        return redirect(url_for("user.profile", uname=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/user_edit_profile.html', form=form)
