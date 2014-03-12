#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
from __future__ import unicode_literals

from flask.ext.assets import (
    Environment,
    ManageAssets,
)

from webassets.filter import register_filter
from webassets_recess import RecessFilter

register_filter(RecessFilter)


__all__ = ['AssetsManager']


class AssetsManager(object):  # pragma: no cover
    def __init__(self, app):
        from bong import settings
        self.app = app
        self.env = Environment(app)
        self.env.url = app.static_url_path
        self.env.load_path.append(self.env.get_directory())
        self.env.set_directory(None)
        self.env.manifest = "file:assets.manifest"
        self.env.auto_build = settings.LOCAL

    def create_bundles(self):
        """Create static bundles and bind them to the `app`

        We are using flask-assets to manage our static stuff, so we just
        need to create named bundles that includes our css and js files.

        Currently, we have just two bundles: `main_css` and `main_js`.
        """
        from bong.web.assets import BUNDLES

        for name, bundle in BUNDLES:
            self.env.register(name, bundle)

    def create_assets_command(self, manager):
        """Create the `assets` command in Flask-Script
        """
        manager.add_command('assets', ManageAssets(self.env))
