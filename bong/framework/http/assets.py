#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals
import re
import imp
from flask.ext.assets import (
    Environment,
    ManageAssets,
)
from webassets.filter import register_filter
from webassets_recess import RecessFilter

register_filter(RecessFilter)

from plant import Node
from bong.settings import bong_path

__all__ = ['AssetsManager']

# disabling test coverage here for now because we don't need assets
# yet.


class AssetsManager(object):  # pragma: no cover
    def __init__(self, app):
        self.app = app
        self.env = Environment(app)
        self.env.url = app.static_url_path
        self.env.load_path.append(self.env.get_directory())
        self.env.set_directory(None)
        self.find_bundles()

    def get_module_name(self, node):
        pattern = r'.*bong/(\w+)/assets.py'
        replacement = 'bong.\g<1>.assets'
        return re.sub(pattern, replacement, node.path).replace('/', '.')

    def import_node(self, node):
        module_name = self.get_module_name(node)

        if 'bong.framework' in module_name:
            return None

        if 'bong.base' in module_name:
            return None

        return imp.load_source(module_name, node.path)

    def find_bundles(self):
        bong_node = Node(bong_path)

        for assetpy in bong_node.find_with_regex("assets.py"):
            module = self.import_node(assetpy)
            BUNDLES = getattr(module, 'BUNDLES', [])
            for name, bundle in BUNDLES:
                self.env.register(name, bundle)

    def create_assets_command(self, manager):
        """Create the `assets` command in Flask-Script
        """
        manager.add_command('assets', ManageAssets(self.env))
