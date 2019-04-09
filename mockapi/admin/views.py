from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .fields import JsonEditorTextAreaField


class MockEndpointView(ModelView):

    can_export = True
    create_modal = True
    # edit_modal = True

    extra_js = [
        '/static/jquery.json-editor.min.js',
        '/static/admin_common.js',
    ]
    form_overrides = {
        'response_body': JsonEditorTextAreaField
    }
    form_widget_args = {
        'response_body': {
            'rows': 20,
            'cols': 50,
            'style': 'color: black',
            'onkeyup': 'editor.load(getJson())'
        }
    }

    column_editable_list = [
        'title', 'uri', 'method', 'enabled',
        'response_type', 'response_code',
        'namespace',
    ]

    column_exclude_list = ['response_body', 'created', 'updated']
    form_excluded_columns = ['created', 'updated']

    # column_searchable_list = ['title', 'uri', 'namespace']
    column_filters = ['namespace', 'method']

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
    admin.add_view(ModelView(models.Namespace, database.db.session))
