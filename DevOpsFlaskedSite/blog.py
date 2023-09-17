from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from .models import Post
import sqlalchemy
from . import db
import simplejson

blog = Blueprint("blog", __name__)


@blog.route("/posts", methods=["GET"])
def posts():
    posts = Post.query.filter(Post.id.between('1', '3')).all()
    
    

    dicts = []
    response = dict
    
    return str(posts)


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

        