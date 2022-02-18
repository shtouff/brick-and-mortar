from bam import models, types
from bam.extensions import db


def test_crud_users_list_needs_admin(app, token):
    users = [
        models.UserAccount(
            id=i,
            username=f"foo{i}",
            password="foo",
            role=types.Role.USER.value,
        )
        for i in range(10)
    ]
    db.session.add_all(users)
    db.session.commit()

    with app.test_client() as client:
        response = client.get(
            "/api/user",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 403

    with app.test_client() as client:
        response = client.get(
            "/api/user",
            headers={"Authorization": f"Bearer {token(types.Role.ADMIN)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 10
