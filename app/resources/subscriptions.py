from collections import Counter
from urllib.parse import urlparse as link_parse

from app.models.model import Entry, Feed, Folder, FolderFeed, Read, db
from app.resources.entry import Entries
from feedparser import parse as feed_parse
from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse


class Subscriptions(Resource):
    @jwt_required()
    def get(self):
        data = []
        for folder in current_user.folders:
            folder_data = {}
            folder_data["folder"] = folder.name
            folder_data["folder_id"] = folder.id
            folder_list = []
            for feed_id in folder.feeds:
                feed_info = {}
                feed_info["feed_id"] = feed_id.feed.id
                feed_info["title"] = feed_id.feed_alias
                # 用于获取未读订阅个数
                # 需要先建立视图才能使用
                entry_count_query = db.session.execute(
                    f'SELECT entry_count FROM feed_entry_count WHERE feed_id={feed_info["feed_id"]}'
                ).first()
                read_count_query = db.session.execute(
                    f'SELECT count FROM `feed_read_count` WHERE feed_id = {feed_info["feed_id"]} AND user_id ={current_user.id}'
                ).first()
                entry_count = entry_count_query[0] if entry_count_query else 0
                read_count = read_count_query[0] if read_count_query else 0
                feed_info['conut'] = entry_count - read_count
                folder_list.append(feed_info)
                folder_data["folder_list"] = folder_list
            # 修复小bug,前端需要这个列表来获取数量
            if not folder_list:
                folder_data["folder_list"] = folder_list
            data.append(folder_data)
        return jsonify(data=data)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subscription_url',
                            type=str,
                            required=True,
                            help='subscription_url cannot be blank!')
        parser.add_argument('folder_id',
                            type=int,
                            required=True,
                            help='folder_id cannot be blank!')
        parser.add_argument('feed_alias',
                            type=str,
                            help='feed_alias cannot be blank!')
        args = parser.parse_args()
        feed = Feed.query.filter_by(
            feedURL=args['subscription_url']).one_or_none()
        if feed == None:
            d = feed_parse(args['subscription_url']).feed
            alias = args["feed_alias"] or d.title
            feed_info = FolderFeed(feed_alias=alias)
            feed_type = link_parse(d.link).netloc
            feed_info.feed = Feed(d.title, d.subtitle, feed_type, d.link,
                                  args['subscription_url'])
            feed_folder = Folder.query.get(args["folder_id"])
            feed_folder.feeds.append(feed_info)
            db.session.commit()
            return jsonify({'message': 'success!'})
        elif current_user in [
                folder_info.folder.user for folder_info in feed.folders
        ]:
            print("current_user")
            return jsonify({'message': '已经存在了!'})
        else:
            feed_info = FolderFeed(feed_alias=args["feed_alias"] or feed.title)
            feed_info.folder = Folder.query.get(args["folder_id"])
            feed_info.feed = feed
            db.session.add(feed_info)
            db.session.commit()
            return jsonify({'message': 'success!'})

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('feed_id',
                            type=int,
                            required=True,
                            help='feed_id cannot be blank!')
        parser.add_argument('folder_id',
                            type=int,
                            required=True,
                            help='folder_id cannot be blank!')
        parser.add_argument('feed_alias',
                            type=str,
                            help='alias cannot be blank!')
        parser.add_argument('folder_id_dst',
                            type=int,
                            help='alias cannot be blank!')
        args = parser.parse_args()
        feed_info = FolderFeed.query.get((args["folder_id"], args["feed_id"]))
        if args["folder_id"] < 0:
            folder = Folder.query.get(args["folder_id_dst"])
            feed = Feed.query.get(args["feed_id"])
            feed_info = FolderFeed(feed_alias=feed.title)
            feed_info.folder = folder
            feed_info.feed = feed
            db.session.add(feed_info)
            db.session.commit()
            return jsonify({'message': 'success!'})
        if args["folder_id_dst"]:
            if not feed_info:
                return jsonify({'message': 'success!'})
            feed_info.folder = Folder.query.get(args["folder_id_dst"])
        if args["feed_alias"]:
            feed_info.feed_alias = args["feed_alias"]
        db.session.commit()
        return jsonify({'message': 'success!'})

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('feed_id',
                            type=int,
                            required=True,
                            help='feed_id cannot be blank!')
        parser.add_argument('folder_id',
                            type=int,
                            required=True,
                            help='folder_id cannot be blank!')
        args = parser.parse_args()
        feed_info = FolderFeed.query.get((args["folder_id"], args["feed_id"]))
        if feed_info:
            db.session.delete(feed_info)
            db.session.commit()
            return jsonify({'message': 'success!'})
        return jsonify({'message': "don't have this feed!"})
