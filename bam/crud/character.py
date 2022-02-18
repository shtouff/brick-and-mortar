from typing import List

from bam import types, models, schemas


def list(offset: int, limit: int, **filters) -> List[types.Character]:
    q = models.Character.query
    for k, v in filters.items():
        if v:
            q = q.filter(getattr(models.Character, k) == v)

    return schemas.Character.dump(
        [
            types.Character(
                id=c.id,
                name=c.name,
                status=c.status,
                species=c.species,
                type=c.type,
                gender=c.gender,
                episode=([e.id for e in c.episode]),
            )
            for c in q.order_by(models.Character.id).offset(offset).limit(limit)
        ],
        many=True,
    )
