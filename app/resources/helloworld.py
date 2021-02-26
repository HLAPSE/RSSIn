from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
from flask_restful import Resource


class HelloWorld(Resource):
    @jwt_required()
    def get(self):
        return jsonify(user=current_user.name, message="Hello, World!")
