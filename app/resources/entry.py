import datetime
from app.models.model import Feed, Read, db
from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
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
        parser.add_argument('folder_id',
                            type=int,
                            required=True,
                            help='feed_id cannot be blank!')
        args = parser.parse_args()
        entry_list = []
        read_list = [
            read.entry_id
            for read in Read.query.filter_by(user_id=current_user.id).all()
        ]
        if not args["folder_id"]:
            folder_list = [folder for folder in current_user.folders]
            feed_list = []
            for folder in folder_list:
                feed_list += folder.feeds
            # 这里拿到所有的feed
            feeds = [feed.feed for feed in feed_list]
            if args["feed_id"] == -1:
                for feed in feeds:
                    entry_list += feed.entries
            else:
                # 这里是所有未读的文章
                for feed in feeds:
                    entry_list += [
                        entry for entry in feed.entries
                        if entry.id not in read_list
                    ]

        else:
            feed = Feed.query.get(args["feed_id"])
            entry_list = [entry for entry in feed.entries]
        data = []
        for entry in entry_list:
            entry_info = {}
            entry_info["id"] = entry.id
            entry_info["title"] = entry.title
            entry_info["link"] = entry.link
            entry_info["content"] = entry.content
            entry_info["updateddate"] = datetime.datetime.strftime(
                entry.updateddate, "%Y-%m-%d %H:%M:%S")
            entry_info["type"] = entry.feed.type
            entry_info["read"] = True if entry.id in read_list else False
            data.append(entry_info)
        data.sort(key=lambda x: x['updateddate'], reverse=True)
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
        if not Read.query.filter_by(user_id=current_user.id,
                                    entry_id=args["entry_id"]).one_or_none():
            read_record = Read(args["entry_id"])
            current_user.reads.append(read_record)
            db.session.commit()
        return jsonify({'message': 'success!'})
