from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource, reqparse
from ..models.model import User, db


class Users(Resource):

    @jwt_required()
    def get(self):
        # We can now access our sqlalchemy User object via `current_user`.
        return jsonify(id=current_user.id, name=current_user.name,
                        email=current_user.email, logindate=current_user.logindate,
                        createdate=current_user.createdate)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Name cannot be blank!')
        parser.add_argument('email', type=str, required=True,
                            help='email cannot be blank!')
        parser.add_argument('passwd', type=str, required=True,
                            help='passwd cannot be blank!')
        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).one_or_none()
        if user == None:
            new_user = User(
                name=args['name'], email=args['email'], passwd=args['passwd'])
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(email=args['email']).first()
            access_token = create_access_token(identity=user)
            return make_response(jsonify({'message': 'success', 'access_token': access_token, }), 201)
        else:
            return make_response(jsonify({'message': 'Email has existed '}), 200)

    @jwt_required()
    def put(self):
        user = User.query.get(current_user.id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Name cannot be blank!')
        parser.add_argument('email', type=str, required=True,
                            help='email cannot be blank!')
        parser.add_argument('passwd', type=str, required=True,
                            help='passwd cannot be blank!')
        args = parser.parse_args()
        user.name = args['name']
        user.email = args['email']
        user.passwd = args['passwd']
        db.session.commit()
        return make_response(jsonify({'message': 'success!'}), 200)

    @jwt_required()
    def delete(self):
        user = User.query.get(current_user.id)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'message': 'success!'}), 200)
