from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

class UploadForm(FlaskForm):
    csvFile = FileField('csv', default="Click here to upload a CSV File", render_kw={"class": "form-control"})
    submit = SubmitField('Upload', render_kw={"class": "form-control"})