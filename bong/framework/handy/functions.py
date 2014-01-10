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


def get_distance(loc_1, loc_2):
    return (1 * math.sqrt(
        math.pow(
            (69.1 * (loc_1.latitude - loc_2.latitude)), 2) +
        math.pow(
            (53 * (loc_1.longitude - loc_2.longitude)), 2)))


def geo_data_for_ip(ip_address):
    geoip = PyGEOIP(settings.GEO_IP_FILE_LOCATION)
    try:
        return geoip.record_by_addr(ip_address) or EMPTYGEO
    except GeoIPError:
        logger.exception("Failed to get info for ip: %s", ip_address)
        return EMPTYGEO


def get_ip():
    try:
        if request.headers.getlist("X-Real-IP"):
            ip = request.headers.get("X-Real-IP")
            logger.info("Retrieved IP %s from header X-Real-IP", ip)
        elif not request.headers.getlist("X-Forwarded-For"):
            ip = request.remote_addr
            logger.info("Retrieved IP %s from request.remote_addr", ip)
        else:
            ip = request.headers.getlist("X-Forwarded-For")[0]
            logger.info("Retrieved IP %s from header X-Forwarded-For", ip)

        return ip
    except:
        logger.exception("Error retrieving ip address")
        return request.remote_addr
