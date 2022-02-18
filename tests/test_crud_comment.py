from datetime import date

from bam import models, types
from bam.extensions import db


def test_crud_comment_post_without_character_nor_episode(app, token):
    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json={
                "title": "foo",
                "comment": "foo bar baz",
            },
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )

        assert response.status_code == 422


def test_crud_comment_post_with_character(app, token):
    data = {
        "title": "foo",
        "comment": "foo bar baz",
        "character": 1,
    }

    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json=data,
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
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
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 201


def test_crud_comment_post_with_episode(app, token):
    data = {
        "title": "foo",
        "comment": "foo bar baz",
        "episode": 1,
    }

    with app.test_client() as client:
        response = client.post(
            "/api/comment",
            json=data,
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
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
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 201


def test_crud_comment_post_with_episode_and_character(app, token):
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
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
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
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
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
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 201


def test_crud_comment_patch_with_title(app, token):
    data = {
        "title": "bar",
    }

    with app.test_client() as client:
        response = client.patch(
            "/api/comment/1",
            json=data,
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 404

    # create episode and comment
    episode = models.Episode(id=1, name="foo", air_date=date.today(), episode="foo")
    comment = models.Comment(id=1, title="foo", comment="foo bar baz", episode=episode)
    db.session.add_all([episode, comment])
    db.session.commit()

    # retry
    with app.test_client() as client:
        response = client.patch(
            "/api/comment/1",
            json=data,
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 204

    with app.test_client() as client:
        response = client.get(
            "/api/comment/1",
            json=data,
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert response.json["title"] == "bar"


def test_crud_comment_delete(app, token):
    with app.test_client() as client:
        response = client.delete(
            "/api/comment/1",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
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
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 204

    # verify
    with app.test_client() as client:
        response = client.get(
            "/api/comment/1",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 404


def test_crud_comments_paginate(app, token):
    character = models.Character(
        id=1,
        name=f"foo",
        status="foo",
        species="foo",
        gender="foo",
        type="foo",
    )
    comments = [
        models.Comment(
            id=i, title=f"foo{i}", comment="foo bar baz", character=character
        )
        for i in range(10)
    ]
    db.session.add_all([character, *comments])
    db.session.commit()

    with app.test_client() as client:
        response = client.get(
            "/api/comment",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 10  # no pagination asked, use defaults

    with app.test_client() as client:
        response = client.get(
            "/api/comment?offset=2&limit=2",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["id"] == 2
    assert response.json[1]["id"] == 3


def test_crud_comments_filter(app, token):
    characters = [
        models.Character(
            id=i,
            name=f"foo{i}",
            status="foo",
            species="foo",
            gender="foo",
            type="foo",
        )
        for i in range(2)
    ]
    comments = [
        models.Comment(
            id=i, title=f"foo{i}", comment="foo bar baz", character=characters[i]
        )
        for i in range(2)
    ]
    db.session.add_all([*characters, *comments])
    db.session.commit()

    with app.test_client() as client:
        response = client.get(
            "/api/comment",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 2  # no filtering

    with app.test_client() as client:
        response = client.get(
            "/api/comment?character=1",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == 1
