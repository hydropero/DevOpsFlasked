from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from .models import Post, User
import sqlalchemy as sqla
from . import db
import simplejson

blog = Blueprint("blog", __name__)

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

@blog.route("/posts", methods=["GET"])
def posts():
    posts = db.session.execute(sqla.text("SELECT * FROM formatted_post"))
    list_of_posts = []
    [list_of_posts.append(row2dict(post)) for post in posts]
    
    return render_template('posts.html', list_of_posts=list_of_posts)


@blog.route("/create-post", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        post_title = request.form.get('post_title')
        post_subtitle = request.form.get('post_subtitle')
        post_content = request.form.get('post_content')
        post_tags = request.form.get('post_tags')
        post_author = 'Myles Bulla'
        post = Post.query.filter_by(post_title=post_title).first()
        
        if post:
            flash('A post with this title already exists', category="error")
            return redirect(url_for('blog.create_post'))
        if len(post_title) < 5 or len(post_title) > 50:
            flash("Post title must be greater than 5 characters and less than 50", category="error")
        elif len(post_content) < 1:
            flash("Post must contain some content!", category="error")
        elif len(post_subtitle) < 1 or len(post_subtitle) > 50:
             flash("Post must contain some content!", category="error")
        else:
            new_post = Post(
                post_content=post_content,
                post_subtitle=post_subtitle,
                post_title = post_title,
                post_tags = post_tags,
                post_author = post_author,
            )
            db.session.add(new_post)
            db.session.commit()
            flash("Post created!", category="success")
            return redirect(url_for("blog.create_post"))
    else:
        return render_template('create_post.html')

        