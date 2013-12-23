# -*- coding: utf-8; mode: python -*-
from milieu import Environment
import sys

env = Environment()

SELF = sys.modules[__name__]

from os.path import join, abspath


LOCAL_PORT = 8000
PORT = env.get_int('PORT', LOCAL_PORT)

STATIC_BASE_URL = '//static.bong.s3-website-us-east-1.amazonaws.com/s/'

# Identifying environment
LOCAL = PORT is LOCAL_PORT

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
SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI')
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

API_TOKEN_EXPIRATION_TIME = 60 * 60 * 12  # 12 hours in seconds
SALT = 'UXLcFCGwG_7tgC_6'
