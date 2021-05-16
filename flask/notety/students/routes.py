from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from notety import db, bcrypt
from notety.models import Student
from notety import grades, students_collection, data_collection
from notety.students.forms import (RegistrationForm, LoginForm)
import datetime

students = Blueprint('students', __name__)

@students.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    fetched = data_collection.find({}).sort("class_name", 1)
    form.class_name.choices = [(None, 'Choose the class you belong to')]
    form.class_name.choices += [(_class["class_name"], _class["class_name"]) for _class in fetched]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = {
            "f_name": form.f_name.data,
            "l_name": form.l_name.data,
            "class_name": form.class_name.data,
            "cin": form.cin.data,
            "email": form.email.data,
            "password": hashed_password,
            "inscription_date": datetime.datetime.now()
        }
        students_collection.insert_one(student)
        
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('students.login'))

    return render_template('students/register.html', title='Register', form=form)



@students.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user= students_collection.find_one({'email': form.email.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
                username = user['f_name'] + " " + user['l_name']
                email = user['email']
                cin = user['cin']
                
                user = Student(username, email, cin)
                login_user(user, remember=form.remember.data)

                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Please check email and password', 'danger')
    return render_template('students/login.html', title='Login', form=form)

@students.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('students.login'))


@students.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title='Account')




@students.route("/student/grades", methods=['GET', 'POST'])
@login_required
def get_result():
    grade = grades.find_one( {'student.cin': current_user.cin} )

    if grade is None:
        return render_template('students/grades.html', title='Consult Your Grades', results=False)
    
    sem1_modules = grade['sem1']
    sem2_modules = grade['sem2']


    return render_template('students/grades.html', title='Consult Your Grades', results=True, modules1=sem1_modules, modules2=sem2_modules)