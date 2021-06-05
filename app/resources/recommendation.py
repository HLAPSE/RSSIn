import re
from app.models.model import Entry, Feed, FolderFeed, User, db
from app.resources import feed, folder
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource, reqparse


def get_similarity(set1, set2):
    union = set.union(set1, set2)
    return len(set1 & set2) / len(union)


# 构建群体
def get_threeuser(res):
    similarity = {}
    tmp = []
    if len(res) < 3:
        tmp = res
    else:
        tmp = [(user_id, value) for (user_id, value) in res[:3]]
    for (user_id, value) in tmp:
        similarity[user_id] = value
    return similarity


class Recommendations(Resource):
    @jwt_required()
    def get(self):
        # 用户已订阅的
        subscriptions = set(feeds_info.feed for folder in current_user.folders
                            for feeds_info in folder.feeds)
        unsubscriptions = set(Feed.query.all()) - subscriptions
        # 假设这个未订阅的就是基于推荐算法得出的
        users = set(user for user in User.query.all())
        user_feed = {}
        for user in users:
            user_feed[user.id] = set(feeds_info.feed.id
                                     for folder in user.folders
                                     for feeds_info in folder.feeds)
        similarity = {}
        for (key, value) in user_feed.items():
            if key != current_user.id:
                similarity[key] = get_similarity(value,
                                                 user_feed[current_user.id])
        res = sorted(similarity.items(), key=lambda x: x[1], reverse=True)
        group = get_threeuser(res)  #相当于构造用户群体
        all_feed = set()  #获取所有群体的订阅
        for user_id in group.keys():
            all_feed = set.union(all_feed, user_feed[user_id])
        item = all_feed - user_feed[current_user.id]  #当前用户未订阅的
        folder_list = []
        for feed in unsubscriptions:
            feed_info = {}
            feed_info["feed_id"] = feed.id
            feed_info["title"] = feed.title
            feed_info['conut'] = len(feed.entries)
            folder_list.append(feed_info)
        return jsonify(folder_list)
        # return jsonify(data="data")