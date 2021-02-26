# -*- coding: utf-8 -*-
"""
    RSSIn
    ~~~~~~~~~~~~~~

    初始化认证模块

    :copyright: (c) 2021 by HLAPSE.
    :license: MIT, see LICENSE_FILE for more details.
"""
from flask_jwt_extended import JWTManager

from app.models.model import User

jwt = JWTManager()


def init_app(app):
    jwt.init_app(app)
    return jwt


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable forma
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loades a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
