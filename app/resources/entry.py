from app.models.model import Entry, Feed, Read
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource, reqparse


class entries(Resource):
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
        entry_list = [entry for entry in feed.entries]
        data = []
        for entry in entry_list:
            entry_info = {}
            entry_info["id"] = entry.id
            entry_info["title"] = entry.title
            entry_info["link"] = entry.link
            entry_info["content"] = entry.content
            entry_info["updateddate"] = entry.updateddate
            data.append(entry_info)
        return jsonify(data=data)

    @jwt_required()
    def put(self):
        """标记已读"""
        parser = reqparse.RequestParser()
        parser.add_argument('entry_id',
                            type=int,
                            required=True,
                            help='feed_id cannot be blank!')
        args = parser.parse_args()
        entry = Entry.query.get(args["entry_id"])
        read_record = Read(entry.feed.id, args["entry_id"])
        current_user.reads.append(read_record)
        return jsonify({'message': 'success!'})