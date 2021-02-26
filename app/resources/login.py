from datetime import datetime

from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from ..models.model import User, db


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True,
                            help='email cannot be blank!')
        parser.add_argument('passwd', type=str, required=True,
                            help='passwd cannot be blank!')
        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).one_or_none()
        if not user or not user.check_password(args['passwd']):
            return jsonify("Wrong username or password")
        user.logindate = datetime.now()
        db.session.commit()
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)
