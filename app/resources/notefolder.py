import re

from app.models.model import Folder, NoteFolder, db
from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse


class NoteFolders(Resource):
    @jwt_required()
    def get(self):
        data = []
        for folder in current_user.notefolders:
            folder_info = {}
            folder_info["name"] = folder.name
            folder_info["id"] = folder.id
            folder_info["note_count"] = folder.note_count
            data.append(folder_info)
        return jsonify(data=data)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('notefolder_name',
                            type=str,
                            required=True,
                            help='notefolder_name cannot be blank!')
        args = parser.parse_args()
        if args["notefolder_name"] not in [
                folder.name for folder in current_user.notefolders
        ]:
            folder = NoteFolder(name=args["notefolder_name"])
            current_user.notefolders.append(folder)
            db.session.commit()
            return jsonify({'message': 'success!'})
        else:
            return jsonify({'message': 'notefolder has existed!'})

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('notefolder_name',
                            type=str,
                            required=True,
                            help='subscription_url cannot be blank!')
        parser.add_argument('notefolder_id',
                            type=int,
                            required=True,
                            help='subscription_url cannot be blank!')
        args = parser.parse_args()
        if args["notefolder_name"] not in [
                folder.name for folder in current_user.notefolders
        ]:
            folder = NoteFolder.query.get(args["notefolder_id"])
            folder.name = args["notefolder_name"]
            db.session.commit()
            return jsonify({'message': 'success!'})
        else:
            return jsonify(
                {'message': args["notefolder_name"] + ' has existed!'})

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('notefolder_id',
                            type=int,
                            required=True,
                            help='notefolder_id cannot be blank!')
        args = parser.parse_args()
        folder = NoteFolder.query.get(args["notefolder_id"])
        if folder and folder.user.id == current_user.id:
            db.session.delete(folder)
            db.session.commit()
            return jsonify({'message': 'success!'})
        else:
            return jsonify({'message': 'notefolder does not exist!'})
