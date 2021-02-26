from app.models.model import Feed, db
from feedparser import parse as feed_parse
from flask_apscheduler import APScheduler

scheduler = APScheduler()


@scheduler.task('interval', id='title', minutes=1, misfire_grace_time=900)
def job1():
    feed_list = [feed for feed in Feed.query.all()]
    for feed in feed_list:
        title = feed_parse(feed.feedURL).feed.title
        if title != feed.title:
            feed.title = title
            db.session.commit()
        else:
            pass


@scheduler.task('cron', id='do_job_2', minute='*')
def job2():
    print('Job 2 executed')
