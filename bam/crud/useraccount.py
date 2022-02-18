from typing import List

from werkzeug.exceptions import Conflict, NotFound

from bam import models, types, auth, schemas
from bam.extensions import db


def create(user: types.UserAccount) -> types.UserAccount:
    dao = models.UserAccount.query.filter_by(username=user.username)
    if dao:
        raise Conflict

    return schemas.UserAccount.dump(
        auth.add_user(user.username, user.password, user.role)
    )


def list() -> List[types.UserAccount]:
    return schemas.UserAccount.dump(
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


def get(user_id) -> types.UserAccount:
    user = models.UserAccount.query.get(user_id)
    if user is None:
        raise NotFound

    return schemas.UserAccount.dump(
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
