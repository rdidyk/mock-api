from flask import Flask

from mockapi import views
from mockapi.common import Route


ROUTES = (

    Route(
        '/v1/mocks/',
        views.mock_collection,
        ['GET']
    ),

    Route(
        '/v1/mocks/<int:mock_id>',
        views.mock_get,
        ['GET'],
        'mock_get'
    ),

    Route(
        '/v1/mocks/',
        views.mock_create,
        ['POST']
    ),

    Route(
        '/v1/mocks/<int:mock_id>',
        views.mock_delete,
        ['DELETE']
    ),

    Route(
        '/v1/mocks/<int:mock_id>',
        views.mock_update,
        ['PUT']
    ),

    Route(
        '/<path:uri>',
        views.endpoint,
        ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']
    ),
)


def register(app: Flask):
    for route in ROUTES:
        app.add_url_rule(
            route.uri, view_func=route.view, methods=route.methods
        )
