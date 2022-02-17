from flask import Flask

from bam.commands import register_commands
from bam.extensions import db, migrate
from bam.routes import register_routes


def create_app() -> Flask:
    app = Flask(__name__)

    db.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)
    register_commands(app)

    return app


app = create_app()
