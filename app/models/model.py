from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp
from app.common.util import formatDatetime

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    #: 用户id，用户名，邮箱、密码，头像，最后登录时间，创建时间
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwd = db.Column(db.String(80), nullable=False)
    logindate = db.Column(db.DateTime,
                          default=datetime.now,
                          onupdate=datetime.now)
    createdate = db.Column(db.DateTime, default=datetime.now)
    reads = db.relationship('Read', backref='user', lazy=True)
    folders = db.relationship('Folder', backref='user', lazy=True)

    # NOTE: In a real application make sure to properly hash and salt passwords
    def check_password(self, password):
        return safe_str_cmp(password, self.passwd)


class FolderFeed(db.Model):
    #: 用户id、订阅源id、用户分类、未读数目，备注说明（=昵称）
    folder_id = db.Column(db.Integer,
                          db.ForeignKey('folder.id'),
                          primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), primary_key=True)
    feed_alias = db.Column(db.String(60))
    feed_unread_count = db.Column(db.Integer, default=0)
    createdate = db.Column(db.DateTime, default=datetime.now)
    feed = db.relationship("Feed", back_populates="folders")
    folder = db.relationship("Folder", back_populates="feeds")


class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    order_id = db.Column(db.Integer, default=0)
    folder_unread_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feeds = db.relationship("FolderFeed", back_populates="folder")


class Feed(db.Model):
    #: 订阅源id、标题、订阅链接、链接、子标题、分类(用于推荐)、类型(用于分类展示)、已更新位置、可用（可达）、最后更新时间
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    feedURL = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.String(80))
    tag = db.Column(db.String(80))
    type = db.Column(db.String(80), nullable=False)
    reachable = db.Column(db.Boolean, nullable=False)
    updateddate = db.Column(db.DateTime,
                            default=datetime.now,
                            onupdate=datetime.now)
    createdata = db.Column(db.DateTime, default=datetime.now)
    entries = db.relationship('Entry', backref='feed', lazy=True)
    folders = db.relationship("FolderFeed", back_populates="feed")

    def __init__(self, title, subtitle, type, link, feedURL):
        self.title = title
        self.subtitle = subtitle
        self.type = type
        self.link = link
        self.feedURL = feedURL
        self.reachable = True


class Entry(db.Model):
    #: 文章id、标题、链接、发布日期、内容、订阅源id
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    link = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    updateddate = db.Column(db.DateTime,
                            default=datetime.now,
                            onupdate=datetime.now)
    publisheddate = db.Column(db.DateTime, nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)

    def __init__(self, title, link, content, publisheddate):
        self.title = title
        self.link = link
        self.content = content
        self.publisheddate = formatDatetime(publisheddate)


class Read(db.Model):
    #: 笔记ID、用户id、订阅源id、文章id(直接uuid3)、笔记、笔记分类、笔记创建时间
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)
    note = db.Column(db.Text)
    category = db.Column(db.String(80), unique=False, nullable=False)
    notecreatedata = db.Column(db.DateTime, unique=False, nullable=False)
    feed = db.relationship("Feed")