from flask import Flask
from marshmallow_dataclass import class_schema
from webargs.flaskparser import use_args

from bam import types
from bam.crud import (
    comment as crud_comment,
    episode as crud_episode,
    character as crud_character,
)


def register_routes(app: Flask):
    @app.route("/api/character")
    def get_characters():
        return crud_character.list()

    @app.route("/api/episode")
    def get_episodes():
        return crud_episode.list()

    @app.route("/api/comment", methods=["POST"])
    @use_args(class_schema(types.Comment))
    def post_comment(comment):
        return crud_comment.create(comment)

    @app.route("/api/comment/<int:comment_id>", methods=["PUT"])
    @use_args(class_schema(types.CommentForUpdate))
    def put_comment(comment, comment_id):
        return crud_comment.update(comment_id, comment)

    @app.route("/api/comment/<int:comment_id>", methods=["GET"])
    def get_comment(comment_id):
        return crud_comment.get(comment_id)

    @app.route("/api/comment/<int:comment_id>", methods=["DELETE"])
    def delete_comment(comment_id):
        return crud_comment.delete(comment_id)

    @app.route("/api/comment")
    def get_comments():
        return crud_comment.list()
