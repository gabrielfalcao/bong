#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals
import sys
import logging
"""Server file that contains the application instance + WSGI container"""
from plant import Node

from bong.framework.core import Application

this_file = Node(__file__)
this_folder = this_file.parent

application = Application.from_env(
    template_folder=this_folder.join('templates'),
    static_folder=this_folder.join('static'),
)

application.enable_session()
application.enable_assets()
application.setup_logging(sys.stderr, logging.DEBUG)

from .web.controllers import module
application.register_blueprint(module)
