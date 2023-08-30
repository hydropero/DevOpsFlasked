from flask import Blueprint, render_template, url_for, request, flash, redirect


blog = Blueprint("blog", __name__)


@blog.route("/blog", methods=["GET"])
def blog():
    return render_template('posts2.html')