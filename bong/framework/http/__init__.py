#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
from __future__ import unicode_literals

import traceback
from flask import Response, request, current_app
from flask.ext.restful import Api as BaseApi
from flask.ext.restful import Resource
from bong import settings
from bong.framework.log import get_logger
from bong.framework.formats import json

logger = get_logger()


def absolute_url(path, scheme=None):
    """returns the full url for the given path. The scheme (http:// or
    https://) is defined inside of settings.SCHEMA which is guessed by
    the PORT environment variable. If the PORT is 443, then the scheme
    will be 'https://'

    Example:

    >>> absolute_url('/deals')
    'http://localhost:5000/deals'
    """
    return "{0}{1}/{2}".format(
        scheme or settings.SCHEMA,
        settings.DOMAIN,
        path.lstrip('/'),
    )


def ssl_absolute_url(path):
    """Just like `absolute_url` but forces the uri scheme to be `https://`
    Example:

    >>> ssl_absolute_url('/deals')
    'https://localhost:5000/deals'
    """
    return absolute_url(path, 'https://')


def set_cors_into_headers(headers, allow_origin, allow_credentials=True, max_age=60 * 5):  # 5 minutes
    """Takes flask.Response.headers and a string contains the origin
    to be allowed and modifies the given headers inline.

    >>> headers = {'Content-Type': 'application/json'}
    >>> set_cors_into_headers(headers, allow_origin='*')
    """
    headers['Access-Control-Allow-Origin'] = allow_origin
    headers['Access-Control-Allow-Headers'] = request.headers.get(
        'Access-Control-Request-Headers', '*')

    headers['Access-Control-Allow-Methods'] = request.headers.get(
        'Access-Control-Request-Method', '*')

    headers['Access-Control-Allow-Credentials'] = (
        allow_credentials and 'true' or 'false')

    headers['Access-Control-Max-Age'] = max_age


def json_representation(data, code, headers):
    set_cors_into_headers(headers, allow_origin='*')
    return json_response(data, code, headers)


def json_response(data, code, headers={}):
    serialized = json.dumps(data, indent=2)
    headers['Content-Type'] = 'application/json'

    for key in headers.keys():
        value = headers.pop(key)
        headers[str(key)] = str(value)

    return Response(serialized, status=code, headers=headers)


class JSONException(Exception):
    """A base exception class that is json serializable.

    Any controller that raise this exception will have it
    automatically logged and handled by the framework.
    """
    status_code = 400

    def as_dict(self):

        return {
            'error': str(self)
        }

    def as_response(self):
        resp = json_response(self.as_dict(), self.status_code)
        set_cors_into_headers(resp.headers, allow_origin='*')
        return resp


class JSONNotFound(JSONException):
    status_code = 404


class JSONResource(Resource):
    representations = {
        'multipart/form-data': json_representation,
        'application/json': json_representation,
        'text/json': json_representation,
    }

    def options(self, *args, **kw):
        resp = current_app.make_default_options_response()
        resp.headers['Content-Type'] = 'application/json'
        set_cors_into_headers(resp.headers, allow_origin='*')
        return resp


class Api(BaseApi):
    def log_error(self, e):
        msg = ("An error happened upon "
               "\033[1;33m{0}"" \033[1;36m`{1}`\033[0m:\n\n"
               "<bong-error>%s\n</bong-error>".format(
                   request.method,
                   request.url))

        logger.error(msg, traceback.format_exc(e))

    def handle_error(self, e):
        if isinstance(e, JSONException):
            return e.as_response()

        self.log_error(e)
        meta = {
            'error': 'internal server error',
        }
        if settings.TESTING:  # pragma: no cover
            meta['traceback'] = traceback.format_exc(e)

        resp = json_response(meta, 500)
        set_cors_into_headers(resp.headers, allow_origin='*')
        return resp
