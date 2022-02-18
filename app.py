import os

from flask import Flask

from bam import models
from bam.commands import register_commands
from bam.errorhandlers import register_errorhandlers
from bam.extensions import db, migrate, jwt
from bam.routes import register_routes


def update_config_from_env(app: Flask):
    """
    Update config from environment, using reasonable default value.
    """

    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": True,  # set it to False in production, to speed-up things
        "JWT_SECRET_KEY": "this-secret-needs-to-be-changed-in-production",
        "JWT_ACCESS_TOKEN_EXPIRES": 3600,
    }

    app.config.update(
        {key: os.environ.get(key, default) for key, default in config.items()}
    )


def create_app() -> Flask:
    app = Flask(__name__)
    update_config_from_env(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Callback function to check if a JWT exists in the revoked table
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = models.RevokedToken.query.filter_by(jti=jti).one_or_none()
        return token is not None

    register_routes(app)
    register_commands(app)
    register_errorhandlers(app)

    return app


app = create_app()
