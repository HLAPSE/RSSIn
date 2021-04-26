from sqlalchemy.sql.operators import json_getitem_op
from app.models.model import Feed, Read, db, NoteFolder, Note
from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse


class Notes(Resource):
    @jwt_required()
    def get(self):
        data = []
        for folder in current_user.notefolders:
            folder_data = {}
            folder_data["folder"] = folder.name
            folder_data["folder_id"] = folder.id
            folder_list = []
            for note in folder.notes:
                note_info = {}
                note_info["note_id"] = note.id
                note_info["content"] = note.content
                note_info["notecreatedata"] = note.notecreatedata
                entry = note.entry
                entry_info = {}
                entry_info["id"] = entry.id
                entry_info["title"] = entry.title
                entry_info["link"] = entry.link
                note_info['entry_info'] = entry_info
                folder_list.append(note_info)
                folder_data["folder_list"] = folder_list
            if not folder_list:
                folder_data["folder_list"] = folder_list
            data.append(folder_data)
        return jsonify(data=data)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content',
                            type=str,
                            required=True,
                            help='content cannot be blank!')
        parser.add_argument('notefolder_id',
                            type=int,
                            required=True,
                            help='notefolder_id cannot be blank!')
        parser.add_argument('entry_id',
                            type=str,
                            required=True,
                            help='entry_id cannot be blank!')
        args = parser.parse_args()
        note = Note(args["entry_id"], args["content"])
        note_folder = NoteFolder.query.get(args["notefolder_id"])
        if note_folder:
            note_folder.notes.append(note)
            db.session.commit()
            return jsonify({'message': 'success!'})
        else:
            return jsonify({'message': '文件夹不存在!'})

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('note_id',
                            type=int,
                            required=True,
                            help='note_id cannot be blank!')
        parser.add_argument('notefolder_id_dst',
                            type=int,
                            help='notefolder_id_dst cannot be blank!')
        parser.add_argument('content',
                            type=str,
                            required=True,
                            help='content cannot be blank!')
        args = parser.parse_args()
        note = Note.query.get(args["note_id"])
        if NoteFolder.query.get(args["notefolder_id_dst"]):
            note.notefolder_id = args["notefolder_id_dst"]
            db.session.commit()
            return jsonify({'message': 'success!'})
        elif args["content"]:
            note.content = args["content"]
            db.session.commit()
            return jsonify({'message': 'success!'})
        else:
            return jsonify({'message': 'error!'})

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('note_id',
                            type=int,
                            required=True,
                            help='note_id cannot be blank!')
        args = parser.parse_args()
        note = Note.query.get(args["note_id"])
        if note:
            db.session.delete(note)
            db.session.commit()
            return jsonify({'message': 'success!'})
        return jsonify({'message': "don't have this note!"})