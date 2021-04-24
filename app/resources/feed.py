from urllib.parse import urlparse as link_parse

from app.common.util import formatDatetime
from app.models.model import Feed, Read, db, Entry
from feedparser import parse as feed_parse
from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse


class Feeds(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subscription_url',
                            type=str,
                            required=True,
                            help='subscription_url cannot be blank!')
        args = parser.parse_args()
        # 这里有点复杂(code)
        # 订阅存在(1)
        # 1.用户未订阅(11)
        # 1.1返回订阅信息
        # 1.2文章信息
        # 2.用户已订阅(12)
        # 2.1返回订阅信息
        # 2.2返回文章信息
        # 订阅不存在(2)
        # 订阅错误(21)
        # 1.返回错误
        # 订阅正常(22)
        # 首先添加订阅,然后
        # 1.返回文章
        # 2.返回订阅信息
        code = 0
        feed = Feed.query.filter_by(
            feedURL=args['subscription_url']).one_or_none()
        try:
            if feed:
                if current_user not in [
                        folder_info.folder.user for folder_info in feed.folders
                ]:
                    code = 11
                else:
                    code = 12
            else:
                # 首先添加订阅
                d = feed_parse(args['subscription_url']).feed
                feed_type = link_parse(d.link).netloc
                feed = Feed(d.title, d.subtitle, feed_type, d.link,
                            args['subscription_url'])
                db.session.add(feed)
                db.session.commit()
                code = 22
                # 然后将订阅文章刷新
                feed = Feed.query.filter_by(
                    feedURL=args['subscription_url']).one_or_none()
                feed_list = [feed]
                for feed in feed_list:
                    feed_updated = formatDatetime(
                        feed_parse(feed.feedURL).feed.updated_parsed)
                    if str(feed.updateddate) != feed_updated:
                        entries = feed_parse(feed.feedURL).entries
                        for entry in entries:
                            article = Entry.query.filter_by(
                                link=entry.link).one_or_none()
                            if article:
                                article_update = formatDatetime(
                                    entry.updated_parsed)
                                if article_update != str(
                                        article.publisheddate):
                                    # 如果文章更新
                                    if hasattr(entry, 'content'):
                                        content = entry.content[0]["value"]
                                    elif hasattr(entry, 'summary'):
                                        content = entry.summary
                                    else:
                                        content = None
                                    article.title = entry.title
                                    article.content = content
                                    article.updateddate = article_update
                                    db.session.commit()
                            else:
                                # 如果文章不存在
                                if hasattr(entry, 'content'):
                                    content = entry.content[0]["value"]
                                elif hasattr(entry, 'summary'):
                                    content = entry.summary
                                else:
                                    content = None
                                feed_entry = Entry(entry.title, entry.link,
                                                   content,
                                                   entry.published_parsed)
                                feed.entries.append(feed_entry)
                                db.session.commit()
                        feed.updateddate = feed_updated
                        db.session.commit()
        finally:
            if not code:
                return jsonify(code=code)
            # 这里返回订阅信息及文章
            else:
                # 第一步获取到订阅信息
                read_list = [
                    read.entry_id for read in Read.query.filter_by(
                        user_id=current_user.id).all()
                ]
                feed = Feed.query.filter_by(
                    feedURL=args['subscription_url']).one_or_none()
                entry_list = [entry for entry in feed.entries]
                feed_info = {}
                feed_info['id'] = feed.id
                feed_info['title'] = feed.title
                feed_info['link'] = feed.link
                feed_info['sub_title'] = feed.subtitle
                feed_info['reachable'] = feed.reachable
                # 第二步获取订阅文章
                data = []
                for entry in entry_list:
                    entry_info = {}
                    entry_info["id"] = entry.id
                    entry_info["title"] = entry.title
                    entry_info["link"] = entry.link
                    entry_info["content"] = entry.content
                    entry_info["updateddate"] = entry.updateddate
                    entry_info["type"] = entry.feed.type
                    entry_info[
                        "read"] = True if entry.id in read_list else False
                    data.append(entry_info)
                return jsonify(code=code, feed_info=feed_info, entries=data)
