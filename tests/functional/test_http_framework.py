#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
from __future__ import unicode_literals
import json
from mock import patch
from bong import settings
from bong.api.resources import api


from bong.framework.http import (
    absolute_url,
    ssl_absolute_url,
    set_cors_into_headers,
    json_representation,
    JSONResource,
    JSONException,
)


@patch('bong.framework.http.request')
def test_api_handle_error_non_json(request):
    ("Api#handle_error should return 500")

    response = api.handle_error(ValueError("boom"))
    response.status_code.should.equal(500)

    data = json.loads(response.data)

    data.should.have.key("error").being.equal("internal server error")


def test_absolute_url():
    ("absolute_url should take a path and return the full url for that path")
    # Background
    settings.SCHEME = 'http://'
    settings.DOMAIN = 'mywebsite.com'

    # Given a path
    path = '/foo/bar'

    # When I call absolute_url on that path
    url = absolute_url(path)

    # Then it should have returned a full URL
    url.should.equal('http://mywebsite.com/foo/bar')


def test_absolute_url_overwriting_scheme():
    ("absolute_url should ignore the settings.SCHEME variable when "
     "it's passed as argument")
    # Background
    settings.SCHEME = 'WRONG://'
    settings.DOMAIN = 'mywebsite.com'

    # Given a path
    path = '/foo/bar'

    # When I call absolute_url passing the scheme
    url = absolute_url(path, scheme='myscheme://')

    # Then it should have returned a full URL
    url.should.equal('myscheme://mywebsite.com/foo/bar')


def test_ssl_absolute_url():
    ("ssl_absolute_url should take a path and return the full url for that path")
    # Background
    settings.SCHEME = 'http://'
    settings.DOMAIN = 'mywebsite.com'

    # Given a path
    path = '/foo/bar'

    # When I call ssl_absolute_url on that path
    url = ssl_absolute_url(path)

    # Then it should have returned a full URL
    url.should.equal('https://mywebsite.com/foo/bar')


@patch('bong.framework.http.request')
def test_set_cors_into_headers(request):
    ("set_cors_into_headers should get `allow-headers` and `allow-methods` from the request")
    request.headers = {}

    # Given that the request header `Access-Control-Request-Headers` is set
    request.headers['Access-Control-Request-Headers'] = 'Content-Type,X-Foo-Bar'

    # And that the request header `Access-Control-Request-Method` is set
    request.headers['Access-Control-Request-Method'] = 'DELETE'

    # When I have an object containing response headers
    response_headers = {}

    # And I call set_cors_into_headers on it
    set_cors_into_headers(response_headers, allow_origin='*')

    # Then the origin should be the one I defined
    response_headers.should.have.key('Access-Control-Allow-Origin').being.equal('*')
    # And the allowed methods are the ones requested
    response_headers.should.have.key('Access-Control-Allow-Methods').being.equal('DELETE')
    # And the allowed headers are the ones requested
    response_headers.should.have.key('Access-Control-Allow-Headers').being.equal('Content-Type,X-Foo-Bar')


@patch('bong.framework.http.request')
def test_json_representation(request):
    ("json_representation should take raw python data to be serialized, "
     "status code and headers and return a CORS-ready json-serialized response")

    # Given some data to be serialized
    data = {
        'foo': 'bar'
    }

    # And some headers
    headers = {
        'header1': 'from-request',
    }

    # When I call the json_representation
    response = json_representation(data, 200, headers)

    # Then it should have returned a response
    response.status_code.should.equal(200)


@patch('bong.framework.http.request')
@patch('bong.framework.http.current_app')
def test_json_resource_has_options_method(current_app, request):
    ("JSONResource should have the method `options` implemented by default and enabling cors")
    request.headers = {}
    request.headers['Access-Control-Request-Headers'] = 'Content-Type,X-Foo-Bar'
    request.headers['Access-Control-Request-Method'] = 'DELETE'

    current_app.make_default_options_response.return_value.headers = {}

    # Given an instance of resource
    rsrc = JSONResource()

    # When I call options
    response = rsrc.options()

    # Then it should be the default options response
    response.headers.should.equal({
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Headers': 'Content-Type,X-Foo-Bar',
        'Access-Control-Allow-Methods': 'DELETE',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Max-Age': 300,
        'Content-Type': 'application/json'
    })


@patch('bong.framework.http.set_cors_into_headers')
def test_json_exception_as_response(set_cors_into_headers):
    ("JSONException should be able to represent itself as a Response")

    exc = JSONException("BOOM")
    response = exc.as_response()

    response.status_code.should.equal(400)
    response.headers.should.have.key('Content-Type').being.equal('application/json')
    response.data.should.equal('{\n  "error": "BOOM"\n}')

    set_cors_into_headers.assert_called_once_with(
        response.headers, allow_origin='*')
