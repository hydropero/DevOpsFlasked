from flask import Blueprint, render_template, url_for, request, flash, redirect
from .models import Post
from . import db

blog = Blueprint("blog", __name__)


@blog.route("/posts", methods=["GET"])
def posts():
    return render_template('test.html')


@blog.route("/create-post", methods=["POST"])
def create_post():

        post_title = request.form.get('post_title')
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
        else:
            new_post = Post(
                post_content=post_content,
                post_title = post_title,
                post_tags = post_tags,
                post_author = post_author,
            )

        db.session.add(new_post)
        db.session.commit()
        flash("Post created!", category="success")
        return redirect(url_for("auth.create_post"))

        