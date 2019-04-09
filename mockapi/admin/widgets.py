from wtforms.widgets import TextArea


class JsonEditorTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', 'json-editor')
        return super().__call__(field, **kwargs)
