from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_login import current_user
from notety.models import Student
from notety import students_collection




class RegistrationForm(FlaskForm):
    f_name = StringField('First name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    l_name = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    

    class_name = SelectField('Select your class',
                           validators=[DataRequired()])

    cin = IntegerField('CIN',
                        validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        student= students_collection.find_one({"cin": self.cin.data})
        if student:
            raise ValidationError('That CIN is taken. Please choose a different one.')

    def validate_email(self, email):
        student= students_collection.find_one({"email": self.email.data})
        if student:
            raise ValidationError('That email is taken. Please choose a different one.')




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
