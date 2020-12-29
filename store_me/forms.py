from datetime import date

from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from store_me.models import Users


class SignUpForm(FlaskForm):
    firstname = StringField('First name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(),
                                    EqualTo('password')])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already exist. Please choose other one.')
    
    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already exist.')
    
    def validate_birthday(self,birthday):
        if birthday.data > date.today():
             raise ValidationError('A birthday cannot be in the future.')


class SignInForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateUserForm(FlaskForm):
    firstname = StringField('First name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    # username = StringField('Username',
    #                         validators=[DataRequired(), Length(min=2, max=20)])
    # email = StringField('Email',
    #                     validators=[DataRequired(), Email()])
    password = PasswordField('Password')  # can add min and max
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])  #can add min and max
    birthday = DateField('Birthday',
                        format='%Y-%m-%d')
    save = SubmitField('Save')
    delete = SubmitField('Delete')

    def validate_birthday(self,birthday):
        if birthday.data > date.today():
             raise ValidationError('A birthday cannot be in the future.')


class SearchProductForm(FlaskForm):
    search_txt = StringField('Search for a product',
                            validators=[DataRequired()])
    search = SubmitField('Search')

class AddToCartForm(FlaskForm):
    add = SubmitField('Add to cart')
    