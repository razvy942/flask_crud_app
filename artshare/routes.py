from flask import render_template, url_for, request, flash, redirect, session
from artshare.forms import LoginForm, RegistrationForm
from artshare import app
from artshare.helpers import loggedout_required, login_required
import os


@app.route('/')
def index():
    images = os.listdir(os.path.join(
        app.static_folder, 'assets', 'images'))
    return render_template('index.html', images=images)


@app.route('/register', methods=['GET', 'POST'])
@loggedout_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Flash message to show the user that an account was succesfully built
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
@loggedout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Welcome back {form.email.data}', 'success')
        session['user'] = form.email.data
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/create-post')
@login_required
def create_post():
    return render_template('create-post.html')


@app.route('/profile/<username>')
def profile_view(username):
    return render_template('profile.html')


@app.route('/profile/<username>/followers')
def profile_followers(username):
    return render_template('followers.html')


@app.route('/<path:path>')
def not_found(path):
    return redirect(url_for('index'))

# setting up global variable to check if user is in session
@app.context_processor
def context_processor():
    is_logged_in = 'user' in session
    return dict(is_logged_in=is_logged_in)
