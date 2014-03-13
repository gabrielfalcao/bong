# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from flask.ext.assets import (
    Bundle,
)
from flask import url_for
from webassets.filter.cssrewrite import CSSRewrite
from webassets.filter.jinja2 import Jinja2
from bong.base.assets import angular, bootstrap_js, bootstrap_css
from bong import settings
from plant import Node

static_url = lambda path: "{0}/{1}".format(
    settings.STATIC_BASE_URL.rstrip('/'),
    path.lstrip('/')
)

JINJA_FILTER = Jinja2(context={
    'settings': settings,
    'socketio_namespace': lambda name: settings.absurl(name),
    'url_for': lambda name: url_for(name),
    'image_url': lambda path: static_url("img/{0}".format(path)),
    'angular_template': lambda path: static_url("templates/{0}".format(path)),
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

templates_node = Node(settings.LOCAL_FILE('static/js/templates'))
nodes = templates_node.find_with_regex("[.]html$")


BUNDLES = [
    ('css-web', Bundle(bootstrap_css, web_less,
                       output='build/bong.css')),
    ('js-web', Bundle(
        jquery_js,
        bootstrap_js,
        angular,
        web_scripts,
        output='build/bong.js')),
]
for node in nodes:
    path = node.path.split("/static/js/")[-1]
    source = "/".join(["js", path])
    destination = "/".join(["build", path])
    BUNDLES.append((path, Bundle(source, output=destination)))
