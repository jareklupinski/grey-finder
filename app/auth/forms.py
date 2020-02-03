from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired

class LoginForm(FlaskForm):
    username = StringField(render_kw={"placeholder": "Username", "class": "form-control"}, validators=[DataRequired()])
    password = PasswordField(render_kw={"placeholder": "Password", "class": "form-control"}, validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In', render_kw={"class": "form-control"})
