from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

class UploadForm(FlaskForm):
    csvFile = FileField('csv')
    submit = SubmitField('Upload')