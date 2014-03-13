#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
from __future__ import unicode_literals

"""
bong.commands.core
~~~~~~~~~~~~~~~~~~~~~~

Contains commands for managing the http server in the local environment
"""

import sys
import logging

from flask.ext.script import Command
from werkzeug.serving import run_simple


class RunServer(Command):  # pragma: no cover
    def __init__(self, application):
        self.application = application
        self.application.setup_logging(
            output=sys.stderr,
            level=logging.ERROR
        )

    def run(self):
        run_simple(
            '0.0.0.0', 8000,
            self.application,
            use_reloader=True,
            use_debugger=True,
        )


class Shell(Command):  # pragma: no cover
    def __init__(self, application):
        self.application = application
        self.application.setup_logging(
            output=sys.stderr,
            level=logging.DEBUG
        )

    def run(self):
        try:
            from IPython import embed
        except ImportError:
            msg = ("You need to install \033[32mIPython\033[0m in "
                   "order to use the bong shell\n")
            sys.stderr.write(msg)

        embed()
