from datetime import date

from bam import models
from bam.extensions import db


def test_crud_comment_post_without_character_nor_episode(app):
    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json={
                "title": "foo",
                "comment": "foo bar baz",
            },
        )

        assert response.status_code == 422


def test_crud_comment_post_with_character(app):
    data = {
        "title": "foo",
        "comment": "foo bar baz",
        "character": 1,
    }

    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json=data,
        )
    assert response.status_code == 422

    # create a character
    db.session.add(
        models.Character(
            id=1, name="foo", status="foo", species="foo", gender="foo", type="foo"
        )
    )
    db.session.commit()

    # retry
    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json=data,
        )
    assert response.status_code == 201


def test_crud_comment_post_with_episode(app):
    data = {
        "title": "foo",
        "comment": "foo bar baz",
        "episode": 1,
    }

    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json=data,
        )
    assert response.status_code == 422

    # create an episode
    db.session.add(
        models.Episode(id=1, name="foo", air_date=date.today(), episode="foo")
    )
    db.session.commit()

    # retry
    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json=data,
        )
    assert response.status_code == 201


def test_crud_comment_post_with_episode_and_character(app):
    data = {
        "title": "foo",
        "comment": "foo bar baz",
        "episode": 1,
        "character": 1,
    }

    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json=data,
        )
    assert response.status_code == 422

    # create episode and character
    episode = models.Episode(id=1, name="foo", air_date=date.today(), episode="foo")
    character = models.Character(
        id=1, name="foo", status="foo", species="foo", gender="foo", type="foo"
    )
    db.session.add_all([episode, character])
    db.session.commit()

    # retry
    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json=data,
        )
    assert response.status_code == 422  # episode and character aren't related

    episode.characters = [character]
    character.episode = [episode]
    db.session.add_all([episode, character])
    db.session.commit()

    # retry
    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json=data,
        )
    assert response.status_code == 201


def test_crud_comment_put_with_title(app):
    data = {
        "title": "bar",
    }

    with app.test_client() as client:
        response = client.put(
            "/api/comment/1",
            json=data,
        )
    assert response.status_code == 404

    # create episode and comment
    episode = models.Episode(id=1, name="foo", air_date=date.today(), episode="foo")
    comment = models.Comment(id=1, title="foo", comment="foo bar baz", episode=episode)
    db.session.add_all([episode, comment])
    db.session.commit()

    # retry
    with app.test_client() as client:
        response = client.put(
            "/api/comment/1",
            json=data,
        )
    assert response.status_code == 204

    with app.test_client() as client:
        response = client.get(
            "/api/comment/1",
            json=data,
        )
    assert response.status_code == 200
    assert response.json["title"] == "bar"


def test_crud_comment_delete(app):
    with app.test_client() as client:
        response = client.delete(
            "/api/comment/1",
        )
    assert response.status_code == 404

    # create character and comment
    character = models.Character(
        id=1, name="foo", status="foo", species="foo", gender="foo", type="foo"
    )
    comment = models.Comment(
        id=1, title="foo", comment="foo bar baz", character=character
    )
    db.session.add_all([character, comment])
    db.session.commit()

    # retry
    with app.test_client() as client:
        response = client.delete(
            "/api/comment/1",
        )
    assert response.status_code == 204

    # verify
    with app.test_client() as client:
        response = client.get(
            "/api/comment/1",
        )
    assert response.status_code == 404
