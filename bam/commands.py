import json
from copy import copy
from typing import Dict, Tuple, List

import click
from flask import Flask
from marshmallow_dataclass import class_schema

from bam import types, models
from bam.extensions import db


def _load_and_prepare(
    path: str,
    type_: type,
    model: db.Model,
    field_to_remove: str,
) -> Tuple[List[db.Model], Dict[int, db.Model]]:
    """
    Load a JSON collection of entities from a path, decode it to python, then deserializes it
    to dataclass objects, using marshmallow. Validation comes for free.

    Since those collections are interrelated, they cannot be directly transformed to Model objects, since the ORM
    doesn't know what ids are figuring.
    Create an intermediary version of Model objects where relationships are temporarily blanked, and ready for future
    restoration.

    Finally, return the two collections.
    """
    with open(path) as fp:
        entities = class_schema(type_)().load(json.load(fp), many=True)

    entity_map = {}
    for entity in entities:
        light_entity = copy(entity.__dict__)
        del light_entity[field_to_remove]
        entity_map[entity.id] = model(**light_entity)

    return entities, entity_map


def register_commands(app: Flask):
    @app.cli.command("csv-import")
    @click.argument("episodes_path")
    @click.argument("characters_path")
    def csv_import(episodes_path: str, characters_path: str):
        """
        Import initial CSV files to the DB.
        """

        episodes, episode_map = _load_and_prepare(
            episodes_path, types.Episode, models.Episode, "characters"
        )
        characters, character_map = _load_and_prepare(
            characters_path, types.Character, models.Character, "episode"
        )

        # backtrack: restore relationships between entities
        for episode in episodes:
            episode_map[episode.id].characters = [
                character_map[k] for k in episode.characters
            ]
        for character in characters:
            character_map[character.id].episode = [
                episode_map[k] for k in character.episode
            ]

        for values in episode_map.values(), character_map.values():
            for dao in values:
                db.session.add(dao)
        db.session.commit()
