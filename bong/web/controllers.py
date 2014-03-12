#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@bong.com>
#
from __future__ import unicode_literals
import time
import json
import logging

from bong import settings
from flask import (
    Blueprint,
    render_template,
    session,
    url_for,
)


module = Blueprint('web', __name__)
logger = logging.getLogger('bong.web')


@module.context_processor
def inject_basics():
    return dict(
        settings=settings,
        messages=session.pop('messages', []),
        github_user=session.get('github_user_data', None),
        json=json,
        len=len,
        full_url_for=lambda *args, **kw: settings.absurl(
            url_for(*args, **kw)
        ),
        ssl_full_url_for=lambda *args, **kw: settings.sslabsurl(
            url_for(*args, **kw)
        ),
        static_url=lambda path: "{0}/{1}?{2}".format(
            settings.STATIC_BASE_URL.rstrip('/'),
            path.lstrip('/'),
            time.time()
        ),
    )


@module.route('/')
def index():
    return render_template('index.html')
