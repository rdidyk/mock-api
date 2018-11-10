from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class MockEndpointView(ModelView):

    column_editable_list = [
        'title', 'uri', 'method',
        'response_body', 'response_type', 'response_code'
    ]

    form_excluded_columns = ['created', 'updated']

    form_choices = {
        'method': [
            ('GET', 'GET'),
            ('POST', 'POST'),
            ('PUT', 'PUT'),
            ('DELETE', 'DELETE'),
            ('PATCH', 'PATCH'),
            ('OPTIONS', 'OPTIONS'),
            ('HEAD', 'HEAD'),
            ('PROPFIND', 'PROPFIND'),
        ]
    }


def register(app):
    from mockapi import models, database

    admin = Admin(app, name='mock-api', template_mode='bootstrap3')
    admin.add_view(MockEndpointView(models.MockEndpoint, database.db.session))
