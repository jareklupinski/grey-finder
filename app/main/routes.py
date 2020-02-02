from flask import render_template, flash, redirect, request, url_for
from flask import current_app as app
from flask_login import current_user, login_user, logout_user, login_required
from flask_apscheduler import APScheduler
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from app import db, scheduler
import logging, requests, os

from app.models import User, Picture
from app.main import bp
from app.main.forms import UploadForm
from app.auth.forms import LoginForm, RegistrationForm

from PIL import Image

@bp.route('/')
@bp.route('/index')
def index():
    uploadForm = UploadForm()
    loginForm = LoginForm()
    return render_template('index.html', uploadform=uploadForm, loginform=loginForm)

@bp.route('/upload',methods = ['POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        csvData = form.csvFile.data 
        lines = csvData.read().splitlines()
        app.apscheduler.add_job(func=scheduled_task, trigger='date', args=[current_user.id, lines], id=str(current_user.id) + str(lines[0]))
    return redirect(url_for("main.index"))

def scheduled_task(current_user_id, lines):
    app = scheduler.app
    with app.app_context():
        for line in lines:
            urlString = str(line)
            idIndex = urlString.find("://")
            fileName = str(current_user_id) + "/" + urlString[idIndex+3:] + ".jpg"
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(fileName))
            urlPath = filePath.replace("app/static/", "")
            picture = Picture.query.filter_by(url=urlPath).first()
            if picture is None:
                with open(filePath, "wb") as imageFile:
                    print("Downloading " + str(line))
                    response = requests.get(line)
                    imageFile.write(response.content)
                    imageFile.close()
                    img = Image.open(filePath).convert('L')
                    greyFilePath = filePath.replace(".jpg", "-greyscale.jpg")
                    greyUrlPath = urlPath.replace(".jpg", "-greyscale.jpg")
                    img.save(greyFilePath, "JPEG")
                    picture = Picture(url=urlPath, greyurl=greyUrlPath, width=img.width, height=img.height, user_id=current_user_id)
                    db.session.add(picture)
                    db.session.commit()
