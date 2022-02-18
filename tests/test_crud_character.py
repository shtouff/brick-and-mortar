from bam import models, types
from bam.extensions import db


def test_crud_characters_paginate(app, token):
    characters = [
        models.Character(
            id=i,
            name=f"foo{i}",
            status="foo",
            species="foo",
            gender="foo",
            type="foo",
        )
        for i in range(10)
    ]
    db.session.add_all(characters)
    db.session.commit()

    with app.test_client() as client:
        response = client.get(
            "/api/character",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 10

    with app.test_client() as client:
        response = client.get(
            "/api/character?offset=2&limit=2",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["id"] == 2
    assert response.json[1]["id"] == 3


def test_crud_characters_filter(app, token):
    characters = [
        models.Character(
            id=i,
            name=f"foo{i}",
            status="foo",
            species="foo",
            gender=f"foo{i}",
            type="foo",
        )
        for i in range(2)
    ]
    db.session.add_all(characters)
    db.session.commit()

    with app.test_client() as client:
        response = client.get(
            "/api/character",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 2  # no filtering

    with app.test_client() as client:
        response = client.get(
            "/api/character?gender=foo1",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == 1
