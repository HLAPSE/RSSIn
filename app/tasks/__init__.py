# -*- coding: utf-8 -*-
"""
    RSSIn.task
    ~~~~~~~~~~~~~~

    初始化数据刷新模块
    :copyright: (c) 2021 by HLAPSE.
    :license: MIT, see LICENSE_FILE for more details.
"""
from .apscheduler import scheduler


def init_app(app):
    scheduler.init_app(app)
    scheduler.start()
