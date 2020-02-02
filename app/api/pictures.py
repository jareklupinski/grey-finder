from flask import jsonify, g
from app import db
from app.api import bp
from app.models import User, Picture
from app.api.auth import token_auth

@bp.route('/pictures', methods=['GET'])
@token_auth.login_required
def get_pictures():
    pictures = Picture.query.filter(Picture.user_id == g.current_user.id).all()
    picturesJson = []
    for picture in pictures:
        picturesJson.append(picture.to_dict())
    return jsonify(picturesJson)

