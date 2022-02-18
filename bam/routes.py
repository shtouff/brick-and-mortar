from flask import Flask
from marshmallow_dataclass import class_schema
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

from bam import types
from bam.crud import (
    comment as crud_comment,
    episode as crud_episode,
    character as crud_character,
)


def register_routes(app: Flask):
    @app.route("/api/character")
    @use_kwargs(
        {
            "offset": fields.Int(missing=0),
            "limit": fields.Int(missing=10),
            "status": fields.Str(missing=None),
            "gender": fields.Str(missing=None),
            "species": fields.Str(missing=None),
            "type": fields.Str(missing=None),
        },
        location="querystring",
    )
    def get_characters(**kwargs):
        offset = kwargs.pop("offset")
        limit = kwargs.pop("limit")

        return crud_character.list(offset, limit, **kwargs)

    @app.route("/api/episode")
    def get_episodes():
        return crud_episode.list()

    @app.route("/api/comment", methods=["POST"])
    @use_args(class_schema(types.Comment))
    def post_comment(comment):
        return crud_comment.create(comment)

    @app.route("/api/comment/<int:comment_id>", methods=["PATCH"])
    @use_args(class_schema(types.CommentForUpdate))
    def patch_comment(comment, comment_id):
        return crud_comment.update(comment_id, comment)

    @app.route("/api/comment/<int:comment_id>", methods=["GET"])
    def get_comment(comment_id):
        return crud_comment.get(comment_id)

    @app.route("/api/comment/<int:comment_id>", methods=["DELETE"])
    def delete_comment(comment_id):
        return crud_comment.delete(comment_id)

    @app.route("/api/comment")
    @use_kwargs(
        {
            "offset": fields.Int(missing=0),
            "limit": fields.Int(missing=10),
            "episode": fields.Int(missing=None),
            "character": fields.Int(missing=None),
        },
        location="querystring",
    )
    def get_comments(**kwargs):
        offset = kwargs.pop("offset")
        limit = kwargs.pop("limit")

        kwargs["episode_id"] = kwargs.pop("episode")
        kwargs["character_id"] = kwargs.pop("character")

        return crud_comment.list(offset, limit, **kwargs)
