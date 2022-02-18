from flask import jsonify

from bam import types, models


def list():
    return jsonify(
        [
            types.Episode(
                id=e.id,
                name=e.name,
                episode=e.episode,
                air_date=e.air_date,
                characters=([c.id for c in e.characters]),
            )
            for e in models.Episode.query.all()
        ]
    )
