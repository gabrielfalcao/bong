#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals
from mock import patch
from bong.framework.handy.functions import (
    slugify,
    empty,
    now,
    geo_data_for_ip,
    get_ip,
    GeoIPError,
)


class HeadersStub(dict):
    def getlist(self, key):
        return key in self and [self.get(key)] or []


def test_slufify():
    ("slugify should turn everything inbto lower case and "
     "replace non-alphanumeric characters into dashes")

    slugify('Gabriel Falcão').should.equal('gabriel-falcao')


@patch('bong.framework.handy.functions.datetime')
def test_now_proxies_to_datetime_utcnow(datetime):
    ("api.models.now returns datetime.utcnow()")

    now().should.equal(datetime.utcnow.return_value)


def test_empty_returns_none():
    ("api.models.empty returns None")

    empty().should.be.none


@patch('bong.framework.handy.functions.request')
def test_get_ip(request):
    ("get_ip should return ip from X-Real-IP header")

    # Given request.headers mock
    request.headers = HeadersStub({
        "X-Real-IP": "10.20.30.40",
    })

    # When I get the IP
    addr = get_ip()

    # Then it should be the one coming from the X-Real-IP header
    addr.should.equal("10.20.30.40")


@patch('bong.framework.handy.functions.request')
def test_get_ip_x_forwarded_for(request):
    ("get_ip should fallback to X-Forwarded-For")

    # Given request.headers mock
    request.headers = HeadersStub({
        "X-Forwarded-For": "10.20.30.40",
    })

    # When I get the IP
    addr = get_ip()

    # Then it should be the one coming from the X-Forwarded-For header
    addr.should.equal("10.20.30.40")


@patch('bong.framework.handy.functions.request')
def test_get_ip_remote_addr(request):
    ("get_ip should fallback to request.remote_addr")

    request.remote_addr = "10.20.30.40"
    # Given request.headers mock
    request.headers = HeadersStub({})

    # When I get the IP
    addr = get_ip()

    # Then it should be the one coming from the X-Forwarded-For header
    addr.should.equal("10.20.30.40")


@patch('bong.framework.handy.functions.PyGEOIP')
def test_geo_data_for_ip(PyGEOIP):
    ("geo_data_for_ip returns info from PyGEOIP")

    geoip = PyGEOIP.return_value

    geo_data_for_ip("10.10.20.20").should.equal(
        geoip.record_by_addr.return_value)

    geoip.record_by_addr.assert_called_once_with(
        "10.10.20.20")


@patch('bong.framework.handy.functions.PyGEOIP')
def test_geo_data_for_ip_upon_exception(PyGEOIP):
    ("geo_data_for_ip returns info from PyGEOIP "
     "upon exception")

    geoip = PyGEOIP.return_value

    geoip.record_by_addr.side_effect = GeoIPError("boom")

    geo_data_for_ip("10.20.30.40").should.equal({
        "city": "Somewhere",
        "region_name": "",
        "area_code": "",
        "time_zone": "",
        "dma_code": "",
        "metro_code": "",
        "country_code3": "",
        "latitude": "",
        "postal_code": "",
        "longitude": "",
        "country_code": "WORLD",
        "country_name": "A COUNTRY",
        "continent": "",
    })
