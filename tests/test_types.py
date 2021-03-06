from datetime import date

from bam import types, schemas


def test_episode_with_air_date():
    data = {
        "id": 1,
        "name": "foo",
        "air_date": "December 2, 2013",
        "episode": "foo",
        "characters": [1, 2],
    }
    episode: types.Episode = schemas.Episode.load(data)
    assert episode.name == "foo"
    assert episode.air_date == date(2013, 12, 2)


def test_character():
    data = {
        "id": 1,
        "name": "foo",
        "status": "foo",
        "species": "foo",
        "type": "foo",
        "gender": "foo",
        "episode": [1, 2],
    }
    character: types.Character = schemas.Character.load(data)
    assert character.name == "foo"


def test_character_with_empty_type():
    data = {
        "id": 1,
        "name": "foo",
        "status": "foo",
        "species": "foo",
        "type": "",
        "gender": "foo",
        "episode": [1, 2],
    }
    character: types.Character = schemas.Character.load(data)
    assert character.type == ""


def test_character_with_empty_episodes():
    data = {
        "id": 1,
        "name": "foo",
        "status": "foo",
        "species": "foo",
        "type": "foo",
        "gender": "foo",
        "episode": [],
    }
    character: types.Character = schemas.Character.load(data)
    assert character.episode == []

    del data["episode"]
    character = schemas.Character.load(data)
    assert character.episode == []
