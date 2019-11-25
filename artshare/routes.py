from flask import render_template, url_for, request, flash, redirect, session, jsonify
from artshare.forms import LoginForm, RegistrationForm, CreatePostForm
from artshare import app, bcrypt, db
from artshare.helpers import loggedout_required, login_required
from artshare.models import User, Post


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts, index_active='active')


@app.route('/register', methods=['GET', 'POST'])
@loggedout_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash password before storing into database
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        email = form.email.data
        username = form.username.data
        # creating new User
        avatar = form.choose_avatar.data
        if avatar:
            user = User(username=username, email=email,
                        password=hashed_password, profile_image=avatar)
        else:
            user = User(username=username, email=email,
                        password=hashed_password)
        # adding new user to database
        db.session.add(user)
        db.session.commit()
        # Flash message to show the user that an account was succesfully built
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, signup_active='active')


@app.route('/login', methods=['GET', 'POST'])
@loggedout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.email == form.email.data).first()
        # check if user exists in database and if password is correct
        if not user or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Incorrect email or password', 'danger')
            return redirect(url_for('login'))
        # if everything checks out, log them in and store them inside the session
        flash(f'Welcome back {form.email.data}', 'success')
        session['user'] = user.id
        return redirect(url_for('index'))
    return render_template('login.html', form=form, login_active='active')


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
        author = User.query.filter_by(id=session.get('user', 0)).first()
        post = Post(title=form.title.data, post_image=form.image_path.data,
                    description=form.description.data, author=author)
        db.session.add(post)
        db.session.commit()
        flash(f'Post {post.title} created!', 'success')
        return redirect(url_for('index'))
    return render_template('create-post.html', form=form, create_post_active='active')


@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        flash('Post does not exist', 'danger')
        return redirect(url_for('index'))
    user = User.query.filter_by(id=session.get('user', 0)).first()
    if not user == post.author:
        flash('Can only edit posts made by you', 'danger')
        return redirect(url_for('post_view', username=post.author.username, post_id=post.id))
    form = CreatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.post_image = form.image_path.data
        post.description = form.description.data
        db.session.commit()
        flash('Post updated succesfully', 'success')
        return redirect(url_for('post_view', username=post.author.username, post_id=post.id))

    return render_template('create-post.html', form=form, post=post)


@app.route('/delete/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id)
    author = post.first().author
    user_id = session.get('user', 0)
    if author.id == user_id:
        post.delete()
        db.session.commit()
        flash(f'Post deleted succesfully!', 'success')
    else:
        flash('Error while deleting post', 'danger')
    return redirect(url_for('profile_view', username=author.username))


@app.route('/profile/<username>')
def profile_view(username):
    user = User.query.filter_by(username=username).first()
    # Link in navbar should only be active if the profile viewed is that owned by the user
    if user and session.get('user', 0) == user.id:
        profile_view_active = 'active'
    else:
        profile_view_active = ''
    return render_template('profile.html', user_profile=user, profile_view_active=profile_view_active)


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


@app.route('/like/<post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    if 'user' not in session:
        return jsonify(is_authenticated=False)
    post = Post.query.filter_by(id=post_id).first()
    user = User.query.filter_by(id=session.get('user')).first()
    liked = False
    if user not in post.liked_by:
        post.liked_by.append(user)
        db.session.commit()
        liked = True
    else:
        post.liked_by.remove(user)
        db.session.commit()
    return jsonify(liked=liked, is_authenticated=True)


@app.route('/<path:path>')
def not_found(path):
    return redirect(url_for('index'))

# setting up global variable to check if user is in session
@app.context_processor
def context_processor():
    is_logged_in = 'user' in session
    user = User.query.filter_by(id=session.get('user', 0)).first()
    return dict(is_logged_in=is_logged_in, user=user)
