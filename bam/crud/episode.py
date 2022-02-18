from typing import List

from bam import types, models, schemas


def list() -> List[types.Episode]:
    return schemas.Episode.dump(
        [
            types.Episode(
                id=e.id,
                name=e.name,
                episode=e.episode,
                air_date=e.air_date,
                characters=([c.id for c in e.characters]),
            )
            for e in models.Episode.query.all()
        ],
        many=True,
    )
