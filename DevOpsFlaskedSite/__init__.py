from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
from sqlalchemy_utils import database_exists
from flask_login import LoginManager

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

db = SQLAlchemy()
DB_HOSTNAME = get_env_variable("POSTGRES_HOSTNAME")
DB_USERNAME = get_env_variable("POSTGRES_USER")
DB_PASSWORD = get_env_variable("POSTGRES_PW")
DB_NAME = get_env_variable("POSTGRES_DB")
DB_URL = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'lolololpopopoplolol'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL 
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
    
    from .views import views
    from .auth import auth
    from .models import Post

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    db.init_app(app)
    if database_exists(DB_URL):
        print('database already exists, will not recreate')
    else:
        delete_database(app)
        create_database(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    return app 
def delete_database(app):
    with app.app_context():
        db.drop_all()
        print("dropped all db!")
    
def create_database(app):
    with app.app_context():
        db.create_all()
        print("created db!")

