# -*- coding: utf-8 -*-
"""
    RSSIn.models
    ~~~~~~~~~~~~~~

    models

    :copyright: (c) 2021 by HLAPSE.
    :license: MIT, see LICENSE_FILE for more details.
"""
from app.models.model import db


def init_app(app):
    db.init_app(app)
    db.app = app
    return db
