from app.common.util import formatDatetime
from app.models.model import Entry, Feed, db
from feedparser import parse as feed_parse
from flask_apscheduler import APScheduler
from app.common.util import get_tags

scheduler = APScheduler()


@scheduler.task('interval', id='title', minutes=10, misfire_grace_time=900)
def fresh_feed_info():

    feed_list = [feed for feed in Feed.query.all()]
    for feed in feed_list:
        title = feed_parse(feed.feedURL).feed.title
        if title != feed.title:
            feed.title = title
            db.session.commit()


@scheduler.task('interval', id='tags', minutes=10, misfire_grace_time=900)
def fresh_tags():
    # 过滤掉RSShub生成的内容
    feed_list = [
        feed
        for feed in Feed.query.filter(Feed.subtitle.notlike("%RSSHub%")).all()
    ]
    for feed in feed_list:
        feed.tag = get_tags(feed)
        db.session.commit()


@scheduler.task('interval', id='fresh_entry', minutes=5)
def fresh_entry():
    # 这个任务用于定时刷新文章
    # 如果订阅源未更新，则下一个
    # 订阅源更新，若文章更新则刷新，而后更新订阅源日期
    feed_list = [feed for feed in Feed.query.all()]
    for feed in feed_list:
        feed_updated = formatDatetime(
            feed_parse(feed.feedURL).feed.updated_parsed)
        if str(feed.updateddate) != feed_updated:
            entries = feed_parse(feed.feedURL).entries
            for entry in entries:
                article = Entry.query.filter_by(link=entry.link).one_or_none()
                if article:
                    article_update = formatDatetime(entry.updated_parsed)
                    if article_update != str(article.publisheddate):
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
                    feed_entry = Entry(entry.title, entry.link, content,
                                       entry.published_parsed)
                    feed.entries.append(feed_entry)
                    db.session.commit()
            feed.updateddate = feed_updated
            db.session.commit()
