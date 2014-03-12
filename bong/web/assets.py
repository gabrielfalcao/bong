# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from flask.ext.assets import (
    Bundle,
)
from flask import url_for
from webassets.filter.cssrewrite import CSSRewrite
from webassets.filter.jinja2 import Jinja2
from bong.base.assets import angular, bootstrap_js
from bong import settings


static_url = lambda path: "{0}/{1}".format(
    settings.STATIC_BASE_URL.rstrip('/'),
    path.lstrip('/')
)

JINJA_FILTER = Jinja2(context={
    'settings': settings,
    'socketio_namespace': lambda name: settings.absurl(name),
    'url_for': lambda name: url_for(name),
    'image_url': lambda path: static_url("img/{0}".format(path)),
    'angular_template': lambda path: static_url(path.lstrip('/')),
})

jquery_js = Bundle("vendor/jquery/dist/jquery.js")
web_scripts = Bundle(
    'js/app.*.js', 'js/app.js', filters=JINJA_FILTER)


CSS_FONT_REWRITE = CSSRewrite(replace={
    '../fonts/': settings.FONT_AWESOME_PATH,
    '/static/fonts/': settings.FONT_AWESOME_PATH,
})

web_less = Bundle(
    'less/web.less',
    filters=('less', JINJA_FILTER)
)


BUNDLES = [
    ('css-web', Bundle(web_less,
                       filters=JINJA_FILTER,
                       output='build/bong.css')),
    ('js-web', Bundle(
        jquery_js,
        bootstrap_js,
        angular,
        web_scripts,
        # filters=('uglifyjs', ),
        output='build/bong.js')),
]
