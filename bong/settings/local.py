#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals

# This file sets up the default environment variables for working in
# local environment.

# The reason for this is that in production the app MUST work
# seamlessly after certain required environment variables are set.

# This file is an example of ALL those essential variables.
import os
import uuid
from os.path import abspath, dirname, join

local_file = lambda *path: join(abspath(dirname(__file__)), *path)
project_file = lambda *path: local_file('..', *path)
root_file = lambda *path: project_file('..', *path)


DEFAULT_DB = 'mysql://root@localhost/bong'


def setup_localhost(settings):
    # Relational Database
    os.environ.setdefault('SQLALCHEMY_DATABASE_URI', DEFAULT_DB)


    # REDIS
    # ~~~~~

    # Example of REDIS_URI for localhost:
    #   redis://localhost:6379
    #
    # Example of REDIS_URI for *PRODUCTION*:
    #   redis://redis-server-hostname:6379/verylongpasswordhashireallymeanSHA512

    os.environ.setdefault('REDIS_URI', 'redis://localhost:6379')
    os.environ.setdefault('SESSION_SECRET_KEY', uuid.uuid4().hex)
    settings.STATIC_BASE_URL = '/static/'
