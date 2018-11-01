from flask import jsonify, request
from . import app


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'error Id': request.headers.get('X-TransactionId'),
        'message': 'Not found {}'.format(request.url),
        'error details': error
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(400)
def bad_request(error=None):
    message = {
        'status': 400,
        'error Id': request.headers.get('X-TransactionId'),
        'message': 'Bad request {}'.format(request.url),
        'error details': str(error)
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp


@app.errorhandler(401)
def not_authorized(error=None):
    message = {
        'status': 401,
        'message': 'You are not Authorized {}'.format(request.url)
    }
    resp = jsonify(message)
    resp.status_code = 401
    return resp


@app.errorhandler(403)
def forbidden(error=None):
    message = {
        'status': 403,
        'message': 'Access forbidden {}'.format(request.url)
    }
    resp = jsonify(message)
    resp.status_code = 403
    return resp


@app.errorhandler(405)
def method_not_allowed(error=None):
    message = {
        'status': 405,
        'message': 'No method {}'.format(request.url),
        'error details': str(error)
    }
    resp = jsonify(message)
    resp.status_code = 405
    return resp


@app.errorhandler(500)
def technnical_error(error=None):
    message = {
        'status': 500,
        'message': 'A technical error has occurred. System unable to process request.',
        'error details': str(error)
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp
