import flask
import quart


def apply():
    flask.g = quart.g
    flask.has_request_context = quart.has_request_context
