from bam import auth, types


def test_login(app):
    data = {"username": "foo", "password": "foo"}

    with app.test_client() as client:
        response = client.post("/login", json=data)
    assert response.status_code == 401

    auth.add_user("foo", "foo", types.Role.USER)

    # retry
    with app.test_client() as client:
        response = client.post("/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json


def test_logout(app):
    with app.test_client() as client:
        response = client.post("/logout", json={})
    assert response.status_code == 401

    data = {"username": "foo", "password": "foo"}
    auth.add_user("foo", "foo", types.Role.USER)

    with app.test_client() as client:
        response = client.post("/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    with app.test_client() as client:
        response = client.post(
            "/logout", json={}, headers={"Authorization": f"Bearer {access_token}"}
        )
    assert response.status_code == 200

    # retry
    with app.test_client() as client:
        response = client.post(
            "/logout", json={}, headers={"Authorization": f"Bearer {access_token}"}
        )
    assert response.status_code == 401  # token has been revoked previously
