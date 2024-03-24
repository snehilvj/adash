import flask
import quart


def apply():
    flask.g = quart.g
    flask.request = quart.request
    flask.has_request_context = quart.has_request_context
