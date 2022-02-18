from flask import jsonify
from webargs.flaskparser import abort
from werkzeug.exceptions import NotFound

from bam import types, models
from bam.extensions import db


def create(comment):
    if comment.episode is None and comment.character is None:
        abort(
            422,
            messages={"json": ["episode and character cannot be both undefined."]},
        )

    episode = None
    if comment.episode:
        episode = models.Episode.query.filter_by(id=comment.episode).one_or_none()
        if episode is None:
            abort(422, messages={"json": ["this episode does not exist."]})

    character = None
    if comment.character:
        character = models.Character.query.filter_by(id=comment.character).one_or_none()
        if character and episode and episode not in character.episode:
            abort(
                422,
                messages={"json": ["those episode and character aren't related."]},
            )
        elif character is None:
            abort(422, messages={"json": ["this character does not exist."]})

    dao = models.Comment(
        title=comment.title,
        comment=comment.comment,
        episode=episode,
        character=character,
    )

    db.session.add(dao)
    db.session.commit()

    comment.id = dao.id
    return jsonify(comment), 201


def update(comment_id, new_comment):
    comment = models.Comment.query.filter_by(id=comment_id).one_or_none()
    if comment is None:
        raise NotFound

    if new_comment.title:
        comment.title = new_comment.title
    if new_comment.comment:
        comment.comment = new_comment.comment

    db.session.commit()
    return jsonify(), 204


def list():
    return jsonify(
        [
            types.Comment(
                id=c.id,
                title=c.title,
                comment=c.comment,
                episode=c.episode_id,
                character=c.character_id,
            )
            for c in models.Comment.query.all()
        ]
    )


def get(comment_id):
    comment = models.Comment.query.filter_by(id=comment_id).one_or_none()
    if comment is None:
        raise NotFound

    return jsonify(
        types.Comment(
            id=comment.id,
            title=comment.title,
            comment=comment.comment,
            episode=comment.episode_id,
            character=comment.character_id,
        )
    )


def delete(comment_id):
    comment = models.Comment.query.filter_by(id=comment_id).one_or_none()
    if comment is None:
        raise NotFound

    db.session.delete(comment)
    db.session.commit()
    return jsonify(), 204