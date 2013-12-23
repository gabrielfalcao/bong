#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Bong LLC
#
from __future__ import unicode_literals

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

from .web.controllers import module
application.register_blueprint(module)
