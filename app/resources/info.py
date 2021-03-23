from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource, reqparse
from app.models.model import User, db, Feed


class Infos(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type',
                            type=str,
                            required=True,
                            help='type cannot be blank!')
        parser.add_argument('id',
                            type=int,
                            required=True,
                            help='id cannot be blank!')
        args = parser.parse_args()
        if args['type'] == 'feed':
            if args['id'] > 0:
                feed = Feed.query.get(args["id"])
                return jsonify(id=feed.id,
                               title=feed.title,
                               link=feed.link,
                               sub_title=feed.subtitle,
                               reachable=feed.reachable)
            elif args['id'] == -1:
                return jsonify(id=0,
                               title="ALL",
                               link="#",
                               sub_title="ALL Feed",
                               reachable=True)
            else:
                return jsonify(id=0,
                               title="Unread",
                               link="#",
                               sub_title="Unread Feed",
                               reachable=True)