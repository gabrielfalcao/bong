#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import absolute_import

from flask.ext.assets import (
    Bundle,
)

from bong.base.assets import jquery, angular, bootstrap_js, bootstrap_css

web_scripts = Bundle('js/web/*.coffee', filters=('coffeescript'))
web_css = Bundle('css/web/*.less', filters=('less',))

BUNDLES = [
    ('js-web', Bundle(jquery, angular, bootstrap_js, web_scripts, filters=('jsmin',), output='build/web.js')),
    ('css-web', Bundle(bootstrap_css, web_css, filters=('cssmin',),output='build/web.css')),
]
