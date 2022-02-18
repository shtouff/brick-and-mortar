import pytest
from marshmallow_dataclass import class_schema

from app import create_app
from bam import types
from bam.extensions import db


@pytest.fixture(scope="session")
def episode_schema():
    return class_schema(types.Episode)()


@pytest.fixture(scope="session")
def character_schema():
    return class_schema(types.Character)()


@pytest.fixture(scope="function")
def app():
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
