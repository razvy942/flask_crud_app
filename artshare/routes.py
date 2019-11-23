from flask import render_template, url_for, request, flash, redirect, session
from artshare.forms import LoginForm, RegistrationForm, CreatePostForm
from artshare import app, bcrypt, db
from artshare.helpers import loggedout_required, login_required
from artshare.models import User, Post
import os



@app.route('/')
def index():
    images = os.listdir(os.path.join(
        app.static_folder, 'assets', 'images'))
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
@loggedout_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash password before storing into database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        username = form.username.data
        # creating new User
        user = User(username=username, email=email, password=hashed_password)
        # adding new user to database
        db.session.add(user)
        db.session.commit()
        # Flash message to show the user that an account was succesfully built
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
@loggedout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        # check if user exists in database and if password is correct
        if not user or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Incorrect email or password', 'danger')
            return redirect(url_for('login'))
        # if everything checks out, log them in and store them inside the session
        flash(f'Welcome back {form.email.data}', 'success')
        session['user'] = user.id
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        author = User.query.filter_by(id = session.get('user', 0)).first()
        post = Post(title=form.title.data, post_image=form.image_path.data, description=form.description.data, author=author)
        db.session.add(post)
        db.session.commit()
    return render_template('create-post.html', form=form)


@app.route('/profile/<username>')
def profile_view(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user_profile=user)


@app.route('/profile/<username>/followers')
def profile_followers(username):
    return render_template('followers.html')

@app.route('/<username>/<post_id>')
def post_view(username, post_id):
    # check if valid user and valid post
    user = User.query.filter_by(username=username).first()
    post = Post.query.filter_by(id=post_id).first()
    if (user and post) and post.author.id == user.id:
        return render_template('post.html', post=post)
    
    return render_template('post.html', post=None)

@app.route('/search', methods=['POST'])
def search():
    username = request.form.get('search-users')
    return redirect(url_for('search_users', username=username))

@app.route('/search/<username>')
def search_users(username):
    users = User.query.filter(User.username.like(f'{username}%')).all()
    return render_template('search.html', users=users)


@app.route('/<path:path>')
def not_found(path):
    return redirect(url_for('index'))

# setting up global variable to check if user is in session
@app.context_processor
def context_processor():
    is_logged_in = 'user' in session
    user = User.query.filter_by(id = session.get('user', 0)).first()
    return dict(is_logged_in=is_logged_in, user=user)
