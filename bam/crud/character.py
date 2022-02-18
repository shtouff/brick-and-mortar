from flask import jsonify

from bam import types, models


def list():
    return jsonify(
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
            for c in models.Character.query.all()
        ]
    )
