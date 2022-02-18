from typing import List

from marshmallow_dataclass import class_schema
from werkzeug.exceptions import Conflict, NotFound

from bam import models, types, auth
from bam.extensions import db

schema = class_schema(types.UserAccount)()


def create(user: types.UserAccount) -> dict:
    dao = models.UserAccount.query.filter_by(username=user.username)
    if dao:
        raise Conflict

    return schema.dump(auth.add_user(user.username, user.password, user.role))


def list() -> List[dict]:
    return schema.dump(
        [
            types.UserAccount(
                id=u.id,
                username=u.username,
                password="****obfuscated****",
                role=types.Role(u.role),
            )
            for u in models.UserAccount.query.all()
        ],
        many=True,
    )


def get(user_id) -> dict:
    user = models.UserAccount.query.get(user_id)
    if user is None:
        raise NotFound

    return schema.dump(
        types.UserAccount(
            id=user.id,
            username=user.username,
            password="****obfuscated****",
            role=types.Role(user.role),
        )
    )


def delete(user_id):
    user = models.UserAccount.query.get(user_id)
    if user is None:
        raise NotFound

    db.session.delete(user)
    db.session.commit()
