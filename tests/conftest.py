import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from bam import types
from bam.extensions import db


@pytest.fixture(scope="function")
def app():
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()


@pytest.fixture(scope="session")
def token():

    # need a callback, otherwise we're not in the app context
    def callback(role: types.Role):
        additional_claims = {"role": role.value}
        return create_access_token(
            identity=role.value.lower(), additional_claims=additional_claims
        )

    return callback
