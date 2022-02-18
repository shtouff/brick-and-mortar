from functools import wraps

import bcrypt
from flask_jwt_extended import create_access_token, get_jwt
from werkzeug.exceptions import Unauthorized, Forbidden

from bam import models, types
from bam.extensions import db


def add_user(username: str, password: str, role: types.Role) -> types.UserAccount:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = models.UserAccount(
        username=username, password=hashed.decode("utf-8"), role=role.value
    )

    db.session.add(user)
    db.session.commit()

    return types.UserAccount(
        username=username,
        password=password,
        role=role,
    )


def require_role(role: types.Role):
    """
    A decorator to check if a role is in the token and has the expected value.
    """

    def inner(func):
        @wraps(func)
        def _require_role(*args, **kwargs):
            try:
                token = get_jwt()
                if types.Role(token["role"]) is not role:
                    raise Forbidden
            except (ValueError, KeyError):
                raise Forbidden

            return func(*args, **kwargs)

        return _require_role

    return inner


def login(username: str, password: str) -> str:
    user = models.UserAccount.query.filter_by(username=username).one_or_none()

    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity=username, additional_claims=additional_claims
        )
        return access_token

    raise Unauthorized


def logout():
    jti = get_jwt()["jti"]

    db.session.add(models.RevokedToken(jti=jti))
    db.session.commit()
