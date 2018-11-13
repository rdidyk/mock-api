from flask import abort, make_response, jsonify


def validate_uri(uri):
    if not uri:
        abort(
            make_response(
                jsonify(
                    status='error',
                    message='attribute uri is required',
                ),
                400
            )
        )

    if str(uri).startswith('/v1/mocks/'):
        abort(
            make_response(
                jsonify(
                    status='error',
                    message='invalid uri: {0} (reserved endpoint)'.format(
                        uri,
                    ),
                ),
                400
            )
        )
