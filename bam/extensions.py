from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

__all__ = ["db", "migrate", "jwt"]

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
