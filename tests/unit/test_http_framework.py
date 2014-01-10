#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals
from mock import patch
from bong.framework.http import (
    absolute_url,
    ssl_absolute_url,
    set_cors_into_headers,
    json_representation,
    json_response,
    JSONResource,
    JSONException
)


@patch('bong.framework.http.settings')
def test_absolute_url(settings):
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


@patch('bong.framework.http.settings')
def test_absolute_url_overwriting_scheme(settings):
    ("absolute_url should ignore the settings.SCHEME variable when it's passed as argument")
    # Background
    settings.SCHEME = 'WRONG://'
    settings.DOMAIN = 'mywebsite.com'

    # Given a path
    path = '/foo/bar'

    # When I call absolute_url passing the scheme
    url = absolute_url(path, scheme='myscheme://')

    # Then it should have returned a full URL
    url.should.equal('myscheme://mywebsite.com/foo/bar')


@patch('bong.framework.http.settings')
def test_ssl_absolute_url(settings):
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
    # background: the flask request headers are mocked
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


@patch('bong.framework.http.set_cors_into_headers')
@patch('bong.framework.http.json_response')
def test_json_representation(json_response, set_cors_into_headers):
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
    response.should.equal(json_response.return_value)

    # And json_response was called like expected
    json_response.assert_called_once_with(data, 200, headers)

    # And set_cors_into_headers was called with origin '*'
    set_cors_into_headers.assert_called_once_with({'header1': 'from-request'}, allow_origin='*')



@patch('bong.framework.http.current_app')
@patch('bong.framework.http.set_cors_into_headers')
def test_json_resource_has_options_method(set_cors_into_headers, current_app):
    ("JSONResource should have the method `options` implemented by default and enabling cors")

    # Given an instance of resource
    rsrc = JSONResource()

    # When I call options
    response = rsrc.options()

    # Then it should be the default options response
    response.should.equal(current_app.make_default_options_response.return_value)

    # And set_cors_into_headers should have been called on the response headers
    set_cors_into_headers.assert_called_once_with(response.headers, allow_origin='*')


@patch('bong.framework.http.Response')
@patch('bong.framework.http.json')
def test_json_response(json, Response):
    ("json_response should take raw python data to be serialized, "
     "status code and headers and return a CORS-ready json-serialized response")

    # Given some data to be serialized
    data = {
        'foo': 'bar'
    }

    # And some headers
    headers = {
        'header1': 'from-request',
    }

    # When I call the json_response
    response = json_response(data, 200, headers)

    # Then it should have returned a response
    response.should.equal(Response.return_value)

    # And the response was called like expected
    Response.assert_called_once_with(
        json.dumps.return_value,
        status=200,
        headers={
            'header1': 'from-request',
            'Content-Type': 'application/json',
        }
    )

    # And json.dumps was called with indent=2
    json.dumps.assert_called_once_with({'foo': 'bar'}, indent=2)


def test_json_exception():
    ("JSONException#as_dict should return the error under the `error` key")

    # Given an exception
    exc = JSONException("BOOM")

    # When I turn that into a dictionary
    data = exc.as_dict()

    # Then it should have the key `error` containing the message
    data.should.have.key("error").being.equal("BOOM")


@patch('bong.framework.http.json_response')
def test_json_exception(json_response):
    ("JSONException#as_response should return a json response")

    # Given an exception
    exc = JSONException("BOOM")

    # When I turn that into a response
    data = exc.as_response()

    # Then it should be a response
    data.should.equal(json_response.return_value)

    # And json_response was called appropriately
    json_response.assert_called_once_with({
        'error': 'BOOM'
    }, 400)
