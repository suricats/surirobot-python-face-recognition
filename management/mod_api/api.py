import os
import werkzeug
from flask import Blueprint
from flask_restful import reqparse, Api, Resource, fields, marshal_with

from management import db
from .models import User, Picture
from .utils import save_file, delete_file

from recognition_engine.utils import add_picture, remove_picture

mod_api = Blueprint('api', __name__)
api = Api(mod_api)

user_parser = reqparse.RequestParser()
user_parser.add_argument('firstname', type=str)
user_parser.add_argument('lastname', type=str)

picture_parser = reqparse.RequestParser()
picture_parser.add_argument(
    'picture', type=werkzeug.datastructures.FileStorage, location='files'
)

user_fields = {
    'id': fields.Integer,
    'firstname': fields.String,
    'lastname': fields.String,
}

picture_fields = {
    'id': fields.Integer,
    'path': fields.String,
    'user_id': fields.Integer,
}


# User
# shows a single user item and lets you delete a user item
class UserApi(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        return user

    def delete(self, user_id):
        user = User.query.get(user_id)

        for picture in user.pictures:
            delete_file(picture.path)
            db.session.delete(picture)

        db.session.delete(user)
        db.session.commit()
        return '', 204

    @marshal_with(user_fields)
    def put(self, user_id):
        args = user_parser.parse_args()
        user = User.query.get(user_id)
        user.firstname = args['firstname']
        user.lastname = args['lastname']
        db.session.add(user)
        db.session.commit()
        return user, 201


# UserList
# shows a list of all users, and lets you POST to add new users
class UserListApi(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User(firstname=args['firstname'], lastname=args['lastname'])
        db.session.add(user)
        db.session.commit()
        return user, 201


# Picture
# shows a single picture item and lets you delete a picture item
class PictureApi(Resource):
    @marshal_with(picture_fields)
    def get(self, user_id, picture_id):
        picture = Picture.query.get(picture_id)
        return picture

    def delete(self, user_id, picture_id):
        picture = Picture.query.get(picture_id)

        remove_picture(picture)

        delete_file(picture.path)
        db.session.delete(picture)
        db.session.commit()
        return '', 204

    @marshal_with(picture_fields)
    def put(self, user_id, picture_id):
        picture = Picture.query.get(picture_id)
        args = picture_parser.parse_args()

        picture_path = save_file(args['picture'])
        delete_file(picture.path)
        picture.path = picture_path

        db.session.add(picture)
        db.session.commit()
        return picture, 201


# PictureList
# shows a list of picture, by user
class PictureListApi(Resource):
    @marshal_with(picture_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        pictures = user.pictures
        return pictures

    @marshal_with(picture_fields)
    def post(self, user_id):
        user = User.query.get(user_id)
        args = picture_parser.parse_args()

        picture_path = save_file(args['picture'])
        picture = Picture(user=user, path=picture_path)

        db.session.add(picture)
        db.session.commit()

        add_picture(picture)

        return picture, 201


# Register routing
api.add_resource(UserListApi, '/users')
api.add_resource(UserApi, '/users/<int:user_id>')
api.add_resource(PictureListApi, '/users/<int:user_id>/pictures')
api.add_resource(PictureApi, '/users/<int:user_id>/pictures/<int:picture_id>')
