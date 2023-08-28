from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html", user=current_user)

@views.route('posts')
def posts():
    return render_template('posts2.html')
 