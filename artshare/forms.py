from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from artshare.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=5, max=20)], render_kw={'placeholder': 'Enter a username between 5 and 20 characters'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={
                        'placeholder': 'Enter an email address'})
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=5)], render_kw={'placeholder': 'Enter password of at least 5 characters'})
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    choose_avatar = StringField('Avatar', render_kw={
                                'placeholder': 'Enter url for custom avatar, othwerwise default is assigned'})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('User with this email already exists')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={
                        'placeholder': 'Enter your email address'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
                             'placeholder': 'Enter your password'})
    submit = SubmitField('Sign In')


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(
        max=150)], render_kw={'placeholder': 'Enter a title for your post'})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={
                                'placeholder': 'Enter a description for your post'})
    image_path = StringField('Image Path', validators=[DataRequired()], render_kw={
                             'placeholder': 'Enter a image url'})
    submit = SubmitField('Create Post')
