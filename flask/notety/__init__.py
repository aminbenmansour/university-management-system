from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from notety.config import Config

#client = MongoClient("localhost", 27017, tls=True, tlsAllowInvalidCertificates=True)
client = MongoClient(host="mongodb",
                     port=27017, 
                     username="root",
                     password="example", 
                     authSource="admin")

db = client["students-grades-management"]

students_collection = db['student']
admin_collection = db['admin']
data_collection = db['data']
grades = db['grades']


data = {
    "class_name": None,
    "sem1": [
    ],
    "sem2": [
    ]
}


grades = db['grades']

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'students.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    #db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from notety.students.routes import students
    from notety.admin.routes import admin
    from notety.main.routes import main
    from notety.errors.handlers import errors

    app.register_blueprint(students)
    app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
