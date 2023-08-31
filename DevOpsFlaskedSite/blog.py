from flask import Blueprint, render_template, url_for, request, flash, redirect


blog = Blueprint("blog", __name__)


@blog.route("/posts", methods=["GET"])
def posts():
    return render_template('test.html')