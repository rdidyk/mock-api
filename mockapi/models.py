from datetime import datetime

from flask import json
from sqlalchemy.event import listens_for

from mockapi.database import db


class TimestampMixin:
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow,
    )
    updated = db.Column(
        db.DateTime, default=datetime.utcnow,
    )


class MockEndpoint(TimestampMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    namespace_id = db.Column(
        db.Integer,
        db.ForeignKey('namespace.id'),
        nullable=True,
    )

    title = db.Column(db.String(80), nullable=False)
    uri = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), default='GET')
    enabled = db.Column(db.Boolean, unique=False, default=True)
    response_body = db.Column(db.Text, nullable=True)
    response_type = db.Column(db.String(100), default='application/json')
    response_code = db.Column(db.Integer, default=200)

    def encode_response_body(self):
        if isinstance(self.response_body, dict):
            self.response_body = json.dumps(self.response_body)

    def __repr__(self):
        return (
            f'<MockEndpoint('
            f'id={self.id}, title={self.title}, '
            f'method={self.method}, uri={self.uri})>'
        )


class Namespace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(120), nullable=False, unique=True)
    endpoints = db.relationship('MockEndpoint', backref='namespace', lazy=True)

    def __repr__(self):
        return f'<Namespace(name={self.name}, path={self.path})'

    def __str__(self):
        return f'ns:{self.path}'


@listens_for(MockEndpoint, 'before_insert')
def pre_insert(mapper, connect, model: MockEndpoint):
    model.encode_response_body()
