from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from .models import Post, User
import sqlalchemy as sqla
from . import db
import simplejson
import markdown
import re

blog = Blueprint("blog", __name__)

def render_links(content):
    matches = re.findall(r"!\[(\w*)\]", content)

    for filename in matches:
        start_filename_index = content.find(filename)
        end_filename_index = (start_filename_index + len(filename) + 1)
        end_of_url = content.find(")", end_filename_index) + 1
        content = content[:end_filename_index] + content[end_of_url:]

        content = content.replace(f"![{filename}]", f"![](images/_resources/{filename}/)")
    return content

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

@blog.route("/posts", methods=["GET"])
def posts():
    posts = db.session.execute(sqla.text("SELECT * FROM formatted_post"))
    list_of_dict_posts = []
    list_of_posts = posts.mappings().all()
    for post in list_of_posts:
        list_of_dict_posts.append(dict(post))

    for post in list_of_dict_posts:
        post.update((k, markdown.markdown(v)) for k, v in post.items() if k == "short_description")

    return render_template('posts.html', list_of_dict_posts=list_of_dict_posts)

@blog.route("/blog_post/<int:post_id>", methods=["GET"])
def blog_post(post_id):
    post = db.session.execute(sqla.text(f"SELECT * FROM formatted_post WHERE id = {post_id}"))
    post_deserialized = dict(post.mappings().all()[0])
    print(post_deserialized)
    print(type(post_deserialized))
    post_deserialized.update((k, markdown.markdown(v)) for k, v in post_deserialized.items() if k == "post_content")
    # this is to replace existing image links dynamically for ease
    post_content_test = post_deserialized["post_content"]
    if "https://mylesdomain.com/images/" in post_deserialized["post_content"]:
        post_deserialized["post_content"] = re.sub("!\[.*\]\(", "![](", post_deserialized["post_content"])
        post_content_test = re.sub("!\[.*\]\(", "![](", post_deserialized["post_content"])
        # this is to ensure the variable exists regardless of whether the if statement executes
    
    post_deserialized["post_content"] = render_links(post_deserialized["post_content"]) 
    post_deserialized.update((k, markdown.markdown(v)) for k, v in post_deserialized.items() if k == "post_content") 
    
    return render_template('blogpost.html', post=post_deserialized)


@blog.route("/create-post", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        try:
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
        except BaseException as e:
                print(e)
                return str(e)
        else:
            try:
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
            except BaseException as e:
                print(e)
                return str(e)
    else:
        return render_template('create_post.html')

        
