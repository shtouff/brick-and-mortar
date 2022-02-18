from datetime import date

from bam import models, types
from bam.extensions import db


def test_crud_episodes(app, token):
    episodes = [
        models.Episode(id=i, name=f"foo{i}", air_date=date.today(), episode="foo")
        for i in range(10)
    ]
    db.session.add_all(episodes)
    db.session.commit()

    with app.test_client() as client:
        response = client.get(
            "/api/episode",
            headers={"Authorization": f"Bearer {token(types.Role.USER)}"},
        )
    assert response.status_code == 200
    assert len(response.json) == 10
