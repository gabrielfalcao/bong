#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@nacaolivre.org>
#
import json
from datetime import datetime, date, time

from bong.framework.formats.json import json_converter, loads, dumps



def test_json_converter_should_convert_datetime():
    ("db.json_converter should know how to serialize datetime objects")

    # Given a datetime object
    obj = datetime(2010, 10, 10, 10, 10, 10)

    # When I serialize it as json
    serialized = json.dumps(obj, default=json_converter)

    # Then it should be a string
    serialized.should.equal('"2010-10-10T10:10:10"')


def test_json_converter_should_convert_date():
    ("db.json_converter should know how to serialize date objects")

    # Given a date object
    obj = date(2010, 10, 10)

    # When I serialize it as json
    serialized = json.dumps(obj, default=json_converter)

    # Then it should be a string
    serialized.should.equal('"2010-10-10"')


def test_json_converter_should_convert_time():
    ("db.json_converter should know how to serialize time objects")

    # Given a time object
    obj = time(10, 10, 10)

    # When I serialize it as json
    serialized = json.dumps(obj, default=json_converter)

    # Then it should be a string
    serialized.should.equal('"10:10:10"')



def test_json_converter_should_yield_string():
    ("db.json_converter should simply fall back to stringify the content")

    # Given a time object
    obj = type('S', (object, ), {'__str__': lambda self: 'COOL'})()

    # When I serialize it as json
    serialized = json.dumps(obj, default=json_converter)

    # Then it should be a string
    serialized.should.equal('"COOL"')


def test_loads_is_proxy_to_real_json_loads():
    ("framework.formats.json.loads should be a proxy to json.loads")

    loads('{"FOO": "BAR"}').should.equal({'FOO':'BAR'})


def test_dumps_sets_default_json_converter():
    ("framework.formats.json.loads should be a proxy to json.loads")

    dumps({'something': 'here'}, indent=5).should.equal('{\n     "something": "here"\n}')
