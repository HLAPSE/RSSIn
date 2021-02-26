# -*- coding: utf-8 -*-
"""
    RSSIn
    ~~~~~~~~~~~~~~

    初始化flask各个功能模块，应用程序的入口

    :copyright: (c) 2021 by HLAPSE.
    :license: MIT, see LICENSE_FILE for more details.
"""
from flask import Flask
from flask_migrate import Migrate

from app import models, resources, auth, tasks


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db = models.init_app(app)
    migrate = Migrate(app, db)
    resources.init_app(app)
    auth.init_app(app)
    tasks.init_app(app)
    return app
