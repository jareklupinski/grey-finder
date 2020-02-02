from flask import redirect, url_for
from flask_login import login_user, logout_user, current_user

from app import db
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
        if not user.check_password(form.password.data):
            return redirect(url_for('main.index'))
        login_user(user)
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
