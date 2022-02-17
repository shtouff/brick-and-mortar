from flask import Flask, jsonify

from bam import models, types


def register_routes(app: Flask):
    @app.route("/api/character")
    def get_characters():
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

    @app.route("/api/episode")
    def get_episodes():
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
