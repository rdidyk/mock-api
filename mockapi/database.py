import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

log = logging.getLogger(__name__)

db = SQLAlchemy()


def register(app):
    db.init_app(app)
    migrate = Migrate(app, db)  # noqa
