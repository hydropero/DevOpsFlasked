from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import sqlalchemy_mixins as sql_mix

class BaseModel(db.Model, sql_mix.AllFeaturesMixin):
    __abstract__ = True
    pass

class Post(BaseModel):
    id =  db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.String(), unique=False)
    post_title = db.Column(db.String(200), unique=False)
    post_tags = db.Column(db.String(400), unique=False)
    post_subtitle = db.Column(db.String(300), unique=False)
    post_author = db.Column(db.String(200), unique=False)
    create_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    update_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    comments = db.relationship('Comment')


class User(BaseModel):
    __repr_attrs__ = ['id', 'email', 'password', 'first_name']
    id =  db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    comments = db.relationship('Comment')


class Comment(BaseModel):
    id =  db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String(600), unique=False)
    create_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_update_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    

