# flask packages
from flask import Response, jsonify


def error_to_response(constrained_value) -> Response:
    message = {'error_message': F'Failed to process request due to the \
        following exception: {constrained_value}'}
    return jsonify(data=message), 400
