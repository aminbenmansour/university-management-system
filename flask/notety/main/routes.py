from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
#from notety.models import Post
import types 
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@login_required
def home():
    return render_template('common/home.html', title="Welcome Home")


@main.route("/about")
@login_required
def about():
    return render_template('common/about.html', title='About')


@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('student.login'))

