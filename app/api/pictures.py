from flask import jsonify, request, g
from flask_login import current_user
from app import db
from app.api import bp
from app.models import User, Picture
from app.api.auth import multi_auth, basic_auth

@bp.route('/all_pictures', methods=['GET'])
@multi_auth.login_required
def get_pictures():
    pictures = Picture.query.filter(Picture.user_id == g.current_user.id).all()
    picturesJson = []
    for picture in pictures:
        picturesJson.append(picture.to_dict())
    return jsonify(picturesJson)

@bp.route('/pictures', methods=['GET'])
@basic_auth.login_required
def get_paginated_pictures():
    if current_user.is_authenticated:
        index = int(request.args.get('start'))
        dimensions = int(request.args.get('dimensions'))
        greyscale = request.args.get('greyscale')
        pictures = Picture.query.filter(Picture.user_id == current_user.id).all()[index:index+10]
        if dimensions > 0:
            pictures = Picture.query.filter(Picture.user_id == current_user.id, Picture.height < dimensions+50, Picture.height > dimensions-50).all()[index:index+10]
        picturesJson = []
        for picture in pictures:
            if greyscale != None:
                picturesJson.append(picture.to_greydict())
            else:
                picturesJson.append(picture.to_dict())
        return jsonify(picturesJson)
    return {}

@bp.route('/picture/<int:index>', methods=['GET'])
@multi_auth.login_required
def get_single_picture(index=0):
    greyscale = request.args.get('greyscale')
    picture = Picture.query.filter(Picture.user_id == g.current_user.id).all()[index]
    picturesJson = []
    if greyscale != None:
        picturesJson.append(picture.to_greydict())
    else:
        picturesJson.append(picture.to_dict())
    return jsonify(picturesJson)

