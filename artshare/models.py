from artshare import db
from datetime import datetime

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
