import os

from flask import Flask

from bam.commands import register_commands
from bam.extensions import db, migrate
from bam.routes import register_routes


def update_config_from_env(app: Flask):
    """
    Update config from environment, using reasonable default value.
    """

    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": True,
    }

    app.config.update(
        {key: os.environ.get(key, default) for key, default in config.items()}
    )


def create_app() -> Flask:
    app = Flask(__name__)
    update_config_from_env(app)

    db.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)
    register_commands(app)

    return app


app = create_app()
