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
    title = db.Column(db.String(80), nullable=False)
    uri = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), default='GET')
    response_body = db.Column(db.Text, nullable=True)
    response_type = db.Column(db.String(100), default='application/json')
    response_code = db.Column(db.Integer, default=200)

    def encode_response_body(self):
        if isinstance(self.response_body, dict):
            self.response_body = json.dumps(self.response_body)

    def __repr__(self):
        return (
            f'<MockEndpoint id={self.id}, title={self.title}, uri={self.uri}>'
        )


@listens_for(MockEndpoint, 'before_insert')
def pre_insert(mapper, connect, model: MockEndpoint):
    model.encode_response_body()
