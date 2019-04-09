from flask import Flask

from mockapi import (
    routes,
    database,
    utils,
    admin,
)


def create_app(config='mockapi/config.yaml'):
    app = Flask(__name__)
    app.config.from_mapping(utils.load_config(config))
    database.register(app)
    routes.register(app)
    admin.views.register(app)
    return app
