from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
from flask_restful import Resource


class HelloWorld(Resource):
    def get(self):
        return jsonify(message="Hello, World!")
