from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from datetime import datetime
from forms import RegistrationForm, LoginForm, LogoutForm

app = Flask(__name__, static_folder='static')

# Secret key for the forms for security such as CSRF attacks, also required for the seesion
app.config['SECRET_KEY'] = 'soen287-assignment3'
# App config to hold the path to the local sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)

# MODELS
liked_posts_association_table = db.Table('liked_posts',
                                         db.Column('user_id', db.Integer,
                                                   db.ForeignKey('user.id')),
                                         db.Column('post_id', db.Integer,
                                                   db.ForeignKey('post.id'))
                                         )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_image = db.Column(
        db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author')
    # Liked posts is a many to many relationship, secondary argument is the association table
    liked_posts = db.relationship(
        'Post', secondary=liked_posts_association_table, backref='liked_by', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    post_image = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login to view page', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def loggedout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


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


if __name__ == "__main__":
    app.run(debug=True)
