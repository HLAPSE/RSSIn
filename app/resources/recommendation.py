from app.resources import feed, folder
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource, reqparse
from app.models.model import Entry, FolderFeed, User, db, Feed


class Recommendations(Resource):
    @jwt_required()
    def get(self):
        # 用户已订阅的
        subscriptions = set(feeds_info.feed for folder in current_user.folders
                            for feeds_info in folder.feeds)
        unsubscriptions = set(Feed.query.all()) - subscriptions
        # 假设这个未订阅的就是基于推荐算法得出的
        folder_list = []
        for feed in unsubscriptions:
            feed_info = {}
            feed_info["feed_id"] = feed.id
            feed_info["title"] = feed.title
            feed_info['conut'] = len(feed.entries)
            folder_list.append(feed_info)
        return jsonify(folder_list)