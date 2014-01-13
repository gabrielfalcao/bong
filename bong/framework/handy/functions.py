#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

import re
import math
import unicodedata
from datetime import datetime

from pygeoip import GeoIP as PyGEOIP
from pygeoip import GeoIPError
from bong import settings
from bong.framework.log import get_logger

from flask import request
logger = get_logger('bong')


def slugify(string):
    normalized = unicodedata.normalize("NFKD", string.lower())
    dashed = re.sub(r'\s+', '-', normalized)
    return re.sub(r'[^\w-]+', '', dashed)


def now():
    return datetime.utcnow()


def empty():
    return None


EMPTYGEO = {
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
}


def geo_data_for_ip(ip_address):
    geoip = PyGEOIP(settings.GEO_IP_FILE_LOCATION)
    try:
        return geoip.record_by_addr(ip_address) or EMPTYGEO
    except GeoIPError:
        logger.exception("Failed to get info for ip: %s", ip_address)
        return EMPTYGEO


def get_ip():
    if request.headers.getlist("X-Real-IP"):
        return request.headers.get("X-Real-IP")
    elif request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]

    return request.remote_addr
