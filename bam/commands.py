import click
from flask import Flask


def register_commands(app: Flask):
    @app.cli.command("csv-import")
    @click.argument("episodes")
    @click.argument("characters")
    def csv_import(episodes: str, characters: str):
        """
        Import initial CSV files to the DB.
        """
        click.secho("imported")
