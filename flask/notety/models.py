import datetime
from flask import current_app
from notety import db, login_manager, students_collection, admin_collection
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_cin):
    try:

        student = students_collection.find_one({"cin": int(user_cin)})

        if student:
            username = student['f_name']+ " " +student['l_name']
            email = student['email']
            cin = student['cin']
            return Student(username, email, cin)

    except ValueError:
        admin = admin_collection.find_one()
        if admin:
            return Admin()
    




class Admin(UserMixin):
    def __init__(self):
        self.username = 'admin'
        self.role = 'admin'

    
    
    def get_id(self):
        object_id = self.username
        return str(object_id)


class Student(UserMixin):
    def __init__(self, username, email, cin):
        self.username = username
        self.email = email
        self.cin = cin
        self.role = 'student'


    def get_id(self):
        object_id = self.cin
        return str(object_id)

