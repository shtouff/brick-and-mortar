import pytest
from marshmallow_dataclass import class_schema

from bam import types


@pytest.fixture(scope="session")
def episode_schema():
    return class_schema(types.Episode)()


@pytest.fixture(scope="session")
def character_schema():
    return class_schema(types.Character)()
