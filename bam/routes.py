from flask import Flask, jsonify
from flask_jwt_extended import jwt_required
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

from bam import types, auth, schemas
from bam.crud import (
    comment as crud_comment,
    episode as crud_episode,
    character as crud_character,
    useraccount as crud_useraccount,
)


def register_routes(app: Flask):
    @app.route("/api/character")
    @jwt_required()
    @use_kwargs(
        {
            "offset": fields.Int(load_default=0),
            "limit": fields.Int(load_default=10),
            "status": fields.Str(load_default=None),
            "gender": fields.Str(load_default=None),
            "species": fields.Str(load_default=None),
            "type": fields.Str(load_default=None),
        },
        location="querystring",
    )
    def get_characters(**kwargs):
        offset = kwargs.pop("offset")
        limit = kwargs.pop("limit")

        return jsonify(crud_character.list(offset, limit, **kwargs))

    @app.route("/api/episode")
    @jwt_required()
    def get_episodes():
        return jsonify(crud_episode.list())

    @app.route("/api/comment", methods=["POST"])
    @jwt_required()
    @use_args(schemas.Comment)
    def post_comment(comment):
        return jsonify(crud_comment.create(comment)), 201

    @app.route("/api/comment/<int:comment_id>", methods=["PATCH"])
    @jwt_required()
    @use_args(schemas.CommentForUpdate)
    def patch_comment(comment: types.CommentForUpdate, comment_id: int):
        crud_comment.update(comment_id, comment)
        return jsonify(), 204

    @app.route("/api/comment/<int:comment_id>", methods=["GET"])
    @jwt_required()
    def get_comment(comment_id: int):
        return jsonify(crud_comment.get(comment_id))

    @app.route("/api/comment/<int:comment_id>", methods=["DELETE"])
    @jwt_required()
    def delete_comment(comment_id: int):
        crud_comment.delete(comment_id)
        return jsonify(), 204

    @app.route("/api/comment")
    @jwt_required()
    @use_kwargs(
        {
            "offset": fields.Int(load_default=0),
            "limit": fields.Int(load_default=10),
            "episode": fields.Int(load_default=None),
            "character": fields.Int(load_default=None),
        },
        location="querystring",
    )
    def get_comments(**kwargs):
        offset = kwargs.pop("offset")
        limit = kwargs.pop("limit")

        kwargs["episode_id"] = kwargs.pop("episode")
        kwargs["character_id"] = kwargs.pop("character")

        return jsonify(crud_comment.list(offset, limit, **kwargs))

    @app.route("/login", methods=["POST"])
    @use_kwargs(
        {
            "username": fields.Str(required=True),
            "password": fields.Str(required=True),
        },
    )
    def post_login(username, password):
        return jsonify({"access_token": auth.login(username, password)})

    @app.route("/logout", methods=["POST"])
    @jwt_required()
    def post_logout():
        auth.logout()
        return jsonify(msg="Access token revoked")

    @app.route("/api/user", methods=["POST"])
    @jwt_required()
    @auth.require_role(types.Role.ADMIN)
    @use_args(schemas.UserAccount)
    def post_user(user):
        return jsonify(crud_useraccount.create(user)), 201

    @app.route("/api/user/<int:user_id>", methods=["GET"])
    @jwt_required()
    @auth.require_role(types.Role.ADMIN)
    def get_user(user_id: int):
        return crud_useraccount.get(user_id)

    @app.route("/api/user/<int:user_id>", methods=["DELETE"])
    @jwt_required()
    @auth.require_role(types.Role.ADMIN)
    def delete_user(user_id):
        crud_useraccount.delete(user_id)
        return jsonify(None), 204

    @app.route("/api/user")
    @jwt_required()
    @auth.require_role(types.Role.ADMIN)
    def get_users():
        return jsonify(crud_useraccount.list())
