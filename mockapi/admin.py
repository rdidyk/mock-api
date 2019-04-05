from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class JsonEditorTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', 'json-editor')
        return super().__call__(field, **kwargs)


class JsonEditorTextAreaField(TextAreaField):
    widget = JsonEditorTextAreaWidget()


class MockEndpointView(ModelView):

    extra_js = [
        '/static/jquery.json-editor.min.js',
        '/static/admin_common.js',
    ]

    column_editable_list = [
        'title', 'uri', 'method',
        'response_type', 'response_code'
    ]
    column_exclude_list = ['response_body', 'created', 'updated']

    form_excluded_columns = ['created', 'updated']

    form_overrides = {
        'response_body': JsonEditorTextAreaField
    }

    form_widget_args = {
        'response_body': {
            'rows': 25,
            'cols': 50,
            'style': 'color: black',
            'onkeyup': 'editor.load(getJson())'
        }
    }

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
