import re
import logging
from datetime import datetime

from flask import (
    abort,
    json,
    jsonify,
    make_response,
    request,
)

from mockapi import models, validators
from mockapi.database import db

log = logging.getLogger(__name__)


def endpoint(uri):
    qs = request.query_string.decode()

    if request.path.startswith('/ns:'):
        namespace = re.search(
            r'^/ns:(?P<ns>[a-zA-Z0-9\-_.]+)/', request.path
        )['ns']
        path = request.path.replace(f'/ns:{namespace}', '')
    else:
        namespace = None
        path = request.path

    if qs:
        requested_uri = f'{path}?{request.query_string.decode()}'
    else:
        requested_uri = path

    if namespace:
        mock = models.MockEndpoint.query.join(
            models.MockEndpoint.namespace,
            aliased=True,
        ).filter(
            models.Namespace.path == namespace,
            models.MockEndpoint.uri == requested_uri,
            models.MockEndpoint.method == request.method,
            models.MockEndpoint.enabled == 1,
        ).first_or_404()
    else:
        mock = models.MockEndpoint.query.filter_by(
            uri=requested_uri,
            method=request.method,
            enabled=1,
            namespace_id=None,
        ).first_or_404()

    resp = make_response(mock.response_body, mock.response_code)
    resp.mimetype = mock.response_type
    return resp


def mock_create():
    body = request.data.decode()

    try:
        data = json.loads(body)
    except Exception:
        return jsonify(
            status='error',
            message='invalid request'
        ), 400

    if 'items' not in data:
        return jsonify(
            status='error',
            message='attribute: items is required'
        ), 400

    if not isinstance(data['items'], list):
        return jsonify(
            status='error',
            message='attribute: items must be type of an array'
        ), 400

    created_items = []
    for item in data['items']:
        uri = item.get('uri')
        validators.validate_uri(uri)
        try:
            m = models.MockEndpoint(
                title=item.get('title'),
                uri=uri,
                method=item.get('method', 'GET'),
                response_body=item.get('response_body'),
                response_type=item.get('response_type'),
                response_code=item.get('response_code', 200),
            )
            db.session.add(m)
        except Exception as e:
            db.session.rollback()
            log.exception(e)
            return jsonify(
                status='error',
                message=str(e)
            ), 406
        else:
            db.session.commit()
            created_items.append(
                {'id': m.id, 'uri': m.uri}
            )
    return jsonify(
        status='success',
        created_items=created_items,
    )


def mock_update(mock_id):
    body = request.data.decode()
    mock = models.MockEndpoint.query.get_or_404(mock_id)

    try:
        data = json.loads(body)
    except Exception:
        return jsonify(
            status='error',
            message='invalid request'
        ), 400

    uri = data.get('uri', mock.uri)

    validators.validate_uri(uri)

    resp_type = data.get('response_type', mock.response_type)
    resp_body = data.get('response_body')

    if mock.response_body != resp_body:
        if resp_body and resp_type.startswith('application/json'):
            resp_body = json.dumps(resp_body)
    else:
        resp_body = mock.response_body

    mock.title = data.get('title', mock.title)
    mock.uri = uri
    mock.method = data.get('method', mock.method)
    mock.response_body = resp_body
    mock.response_type = data.get('response_type', mock.response_type)
    mock.response_code = data.get('response_code', mock.response_code)
    mock.updated = datetime.utcnow()

    try:
        db.session.commit()
    except Exception as e:
        log.exception(e)
        return jsonify(
            status='error',
            message=f'{e}'
        ), 406
    else:
        return jsonify(
            status='success',
        )


def mock_delete(mock_id):
    mock = models.MockEndpoint.query.get_or_404(mock_id)
    db.session.delete(mock)
    db.session.commit()
    return jsonify(
        status='success'
    )


def mock_get(mock_id):
    mock = models.MockEndpoint.query.get_or_404(mock_id)
    return jsonify(
        type="mock_endpoint",
        item=_serialize_mock(mock)
    )


def mock_collection():
    mocks = models.MockEndpoint.query.all()
    return jsonify(
        type="mock_endpoint",
        items=[_serialize_mock(mock) for mock in mocks]
    )


def _serialize_mock(mock):
    if mock.response_type.startswith('application/json'):
        body = json.loads(mock.response_body)
    else:
        body = mock.response_body

    return dict(
        id=mock.id,
        title=mock.title,
        uri=mock.uri,
        method=mock.method,
        response_body=body,
        response_type=mock.response_type,
        response_code=mock.response_code,
        created=mock.created,
        last_update=mock.updated,
    )
