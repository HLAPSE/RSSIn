from app.models.model import Entry, Feed, Read,db
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource, reqparse


class Entries(Resource):
    @jwt_required()
    def get(self):
        # 获取文章列表
        parser = reqparse.RequestParser()
        parser.add_argument('feed_id',
                            type=int,
                            required=True,
                            help='feed_id cannot be blank!')
        args = parser.parse_args()
        feed = Feed.query.get(args["feed_id"])
        read_list = [read.entry_id for read in Read.query.filter_by(user_id=current_user.id)]
        entry_list = [entry for entry in feed.entries]
        data = []
        for entry in entry_list:
            entry_info = {}
            entry_info["id"] = entry.id
            entry_info["title"] = entry.title
            entry_info["link"] = entry.link
            entry_info["content"] = entry.content
            entry_info["updateddate"] = entry.updateddate
            entry_info["read"] = True if entry.id in read_list else False
            data.append(entry_info)
        return jsonify(data=data)

    @jwt_required()
    def post(self):
        """标记已读"""
        parser = reqparse.RequestParser()
        parser.add_argument('entry_id',
                            type=int,
                            required=True,
                            help='feed_id cannot be blank!')
        args = parser.parse_args()
        entry = Entry.query.get(args["entry_id"])
        read_record = Read(args["entry_id"])
        current_user.reads.append(read_record)
        db.session.commit()
        return jsonify({'message': 'success!'})