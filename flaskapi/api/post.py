from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flaskapi import db
from flaskapi.api import api, meta_fields
from flaskapi.models.post import Post
from flaskapi.helpers import paginate

parser = reqparse.RequestParser()
parser.add_argument('title', required=True,
                    help='Title cannot be blank!')
parser.add_argument('content', required=True,
                    help='Content cannot be blank!')
parser.add_argument('contact_id', required=True,
                    type=int,
                    help='ContactId cannot be blank!')

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'date_posted': fields.String,
    'contact_id': fields.Integer
}

post_list_fields = {
    'items': fields.List(fields.Nested(post_fields)),
    'meta': fields.Nested(meta_fields)
}


class PostItem(Resource):
    @marshal_with(post_fields)
    def get(self, id):
        post = Post.query.get_or_404(id)
        return post

    def delete(self, id):
        post = Post.query.get_or_404(id)
        # check permissions
        db.session.delete(post)
        db.session.commit()
        return {}, 204

    @marshal_with(post_fields)
    def put(self, id):
        args = parser.parse_args()
        post = Post.query.get_or_404(id)
        # check permissions
        post.title = args.title
        post.content = args.content
        post.contact_id = args.contact_id
        db.session.commit()
        return post, 201


class PostList(Resource):
    @marshal_with(post_list_fields)
    @paginate()
    def get(self):
        posts = Post.query.order_by(Post.date_posted.desc())
        return posts

    @marshal_with(post_fields)
    def post(self):
        args = parser.parse_args()
        post = Post(title=args.title, content=args.content,
                    contact_id=args.contact_id)
        db.session.add(post)
        db.session.commit()
        return post, 201


api.add_resource(PostList, '/posts')
api.add_resource(PostItem, '/posts/<int:id>')
