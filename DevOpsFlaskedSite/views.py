from flask import Blueprint, render_template
from flask_login import login_required, current_user
import io, csv, boto3

views = Blueprint('views', __name__)

@views.route('/')
def home():
    home_is_active = 'active'
    s3_client = boto3.client('s3')

    s3_object = s3_client.get_object(Bucket="usercounter-devopsblogsite", Key="usercounter.txt")
    # read the file
    data = s3_object['Body'].read().decode('utf-8')

    visitor_count = int(str(data).split('=')[-1])
    visitor_count += 1
    new_visitor_count = f"COUNT={visitor_count}"
    writer_buffer = io.StringIO(new_visitor_count)
    buffer_to_upload = io.BytesIO(writer_buffer.getvalue().encode())
    s3_client.put_object(Body=buffer_to_upload, Bucket='usercounter-devopsblogsite', Key='usercounter.txt')
    return render_template("index.html", user=current_user, home_is_active=home_is_active, visitor_count=str(visitor_count))

@views.route('posts')
def posts():
    return render_template('index.html')
 