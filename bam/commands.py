import json

import click
from flask import Flask
from marshmallow_dataclass import class_schema

from bam import models, types
from bam.extensions import db


def register_commands(app: Flask):
    @app.cli.command("csv-import")
    @click.argument("episodes_path")
    @click.argument("characters_path")
    def csv_import(episodes_path: str, characters_path: str):
        """
        Import initial CSV files to the DB.
        """
        with open(episodes_path) as _f:
            episodes = json.load(_f)
        with open(characters_path) as _f:
            characters = json.load(_f)

        episodes = class_schema(types.Episode)().load(episodes, many=True)
        characters = class_schema(types.Character)().load(characters, many=True)

        for episode in episodes:

            print(episode)
