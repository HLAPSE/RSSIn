from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse
from app.models.model import Folder, db


class Folders(Resource):
    @jwt_required()
    def get(self):
        data = []
        for folder in current_user.folders:
            folder_info = {}
            folder_info["name"] = folder.name
            folder_info["id"] = folder.id
            data.append(folder_info)
        return jsonify(data=data)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('folder_name',
                            type=str,
                            required=True,
                            help='folder_name cannot be blank!')
        args = parser.parse_args()
        if args["folder_name"] not in [
                folder.name for folder in current_user.folders
        ]:
            folder = Folder(name=args["folder_name"])
            current_user.folders.append(folder)
            db.session.commit()
            return jsonify({'message': 'success!'})
        else:
            return jsonify({'message': 'folder has existed!'})

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(' ',
                            type=str,
                            required=True,
                            help='folder_name cannot be blank!')
        parser.add_argument('folder_id',
                            type=int,
                            required=True,
                            help='folder_id cannot be blank!')
        args = parser.parse_args()
        if args["folder_name"] not in [
                folder.name for folder in current_user.folders
        ]:
            folder = Folder.query.get(args["folder_id"])
            folder.name = args["folder_name"]
            db.session.commit()
            return jsonify({'message': 'success!'})
        else:
            return jsonify({'message': args["folder_name"] + ' has existed!'})

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('folder_id',
                            type=int,
                            required=True,
                            help='folder_id cannot be blank!')
        args = parser.parse_args()
        folder = Folder.query.get(args["folder_id"])
        if folder and folder.user.id == current_user.id:
            db.session.delete(folder)
            db.session.commit()
            return jsonify({'message': 'success!'})
        else:
            return jsonify({'message': 'folder does not exist!'})
