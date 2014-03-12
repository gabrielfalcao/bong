#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
from __future__ import unicode_literals, absolute_import

import json
from datetime import date, time, datetime


def json_converter(value):
    date_types = (datetime, date, time)
    if isinstance(value, date_types):
        value = value.isoformat()

    return str(value)


def dumps(data, **kw):
    kw['default'] = json_converter
    return json.dumps(data, **kw)


def loads(*args, **kw):
    return json.loads(*args, **kw)
