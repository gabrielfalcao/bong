#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals

from flask import Response, request, current_app
from flask.ext.restful import Api
from flask.ext.restful import Resource
from bong import settings
from bong.framework.formats import json


def absolute_url(path, scheme=None):
    """returns the full url for the given path. The scheme (http:// or
    https://) is defined inside of settings.SCHEME which is guessed by
    the PORT environment variable. If the PORT is 443, then the scheme
    will be 'https://'

    Example:

    >>> absolute_url('/deals')
    'http://localhost:5000/deals'
    """
    return "{0}{1}/{2}".format(
        scheme or settings.SCHEME,
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
    headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers', '*')
    headers['Access-Control-Allow-Methods'] = request.headers.get('Access-Control-Request-Method', '*')
    headers['Access-Control-Allow-Credentials'] = allow_credentials and 'true' or 'false'
    headers['Access-Control-Max-Age'] = max_age


def json_representation(data, code, headers):
    set_cors_into_headers(headers, allow_origin='*')
    return json_response(data, code, headers)


def json_response(data, code, headers={}):
    serialized = json.dumps(data, indent=2)
    headers['Content-Type'] = 'application/json'
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
        return json_response(self.as_dict(), self.status_code)


class JSONNotFound(JSONException):
    status_code = 404


class JSONResource(Resource):
    representations = {
        'application/json': json_representation,
        'text/json': json_representation,
    }

    def options(self, *args, **kw):
        resp = current_app.make_default_options_response()
        resp.headers['Content-Type'] = 'application/json'
        set_cors_into_headers(resp.headers, allow_origin='*')
        return resp
