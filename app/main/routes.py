from flask import render_template, flash, redirect, request, url_for
from flask import current_app as app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from app import db
import logging, requests, uuid, os

from app.models import User, Picture
from app.main import bp
from app.main.forms import UploadForm

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    pictures = Picture.query.filter(Picture.user_id == current_user.id)
    form = UploadForm()
    return render_template('index.html', title='GreyFinder', pictures=pictures, form=form)

@bp.route('/upload',methods = ['POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        csvData = form.csvFile.data 
        csvLines = csvData.read().splitlines()
        for line in csvLines:
            urlString = str(line)
            idIndex = urlString.find("://")
            fileName = urlString[idIndex+3:] + ".jpg"
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(fileName))
            urlPath = filePath.replace("app/", "")
            picture = Picture.query.filter_by(url=urlPath).first()
            if picture is None:
                with open(filePath, "wb") as imageFile:
                    print("Downloading " + str(line))
                    response = requests.get(line)
                    imageFile.write(response.content)
                    picture = Picture(url=urlPath, user_id=current_user.id)
                    db.session.add(picture)
        db.session.commit()
            
    return redirect(url_for("main.index"))
