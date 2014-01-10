# -*- coding: utf-8; mode: python -*-
from milieu import Environment
import sys

env = Environment()

SELF = sys.modules[__name__]

from os.path import join, abspath


##########
# 3rd party stuff

GOOGLE_ANALYTICS_CODE = 'UA-46592615-1'


##########


LOCAL_PORT = 8000
PORT = env.get_int('PORT', LOCAL_PORT)

#STATIC_BASE_URL = '//static.bong.s3-website-us-east-1.amazonaws.com/s/'
STATIC_BASE_URL = '/static/'

# Identifying environment
LOCAL = PORT is LOCAL_PORT
SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI')

# setting up environment variables after all
if LOCAL:
    print "using custom localhost-specific settings"
    from .local import setup_localhost
    setup_localhost(SELF)

# Detecting environment
PRODUCTION = not LOCAL
DEBUG = not PRODUCTION
TESTING = env.get_bool('TESTING', False)
UNIT_TESTING = env.get_bool('UNIT_TESTING', False)

# HTTP
HOST = env.get("HOST")
DOMAIN = env.get("DOMAIN")
SCHEME = PORT == 443 and 'https://' or "http://"

# Database-related
REDIS_URI = env.get_uri("REDIS_URI")

# Filesystem
LOCAL_FILE = lambda *path: abspath(join(__file__, '..', '..', *path))

# Security
SECRET_KEY = env.get("SESSION_SECRET_KEY")

# Logging
LOGGER_NAMES = [
    'bong',
    'bong.api.models',
    'bong.api.resources',
    'bong.framework.http',
    'bong.framework.db',
    'bong.web.models',
    'bong.web.controllers',
]

SALT = 'SGP#n>*3XJ)E9oubtmf"? bK'
GEO_IP_FILE_LOCATION = LOCAL_FILE('data', 'GeoIPCity.dat')
absurl = lambda *path: "{0}{1}/{2}".format(
    SCHEME, DOMAIN, "/".join(path).lstrip('/'))

sslabsurl = lambda *path: "{0}{1}/{2}".format(
    "https://", DOMAIN, "/".join(path).lstrip('/'))
