# -*- coding: utf-8 -*-
"""
    RSSIn.resources
    ~~~~~~~~~~~~~~

    Restful 风格API的resource

    :copyright: (c) 2021 by HLAPSE.
    :license: MIT, see LICENSE_FILE for more details.
"""
from flask_restful import Api
from .folder import Folders
from .helloworld import HelloWorld
from .login import Login
from .subscriptions import Subscriptions
from .user import Users
from .entry import Entries
from .notefolder import NoteFolders
from .note import Notes
from .info import Infos
from .feed import Feeds
from .recommendation import Recommendations

api = Api()
api.add_resource(HelloWorld, '/')
api.add_resource(Users, '/users')
api.add_resource(Login, '/login')
api.add_resource(Subscriptions, '/subscriptions')
api.add_resource(Folders, '/folders')
api.add_resource(Entries, '/entries')
api.add_resource(NoteFolders, '/notefolders')
api.add_resource(Notes, '/notes')
api.add_resource(Infos, '/infos')
api.add_resource(Feeds, '/feeds')
api.add_resource(Recommendations, '/recommendations')


def init_app(app):
    api.init_app(app)
    return api
