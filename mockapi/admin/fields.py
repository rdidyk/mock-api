from wtforms import TextAreaField

from .widgets import JsonEditorTextAreaWidget


class JsonEditorTextAreaField(TextAreaField):
    widget = JsonEditorTextAreaWidget()
