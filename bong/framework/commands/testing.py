#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals

"""
bong.commands.testing
~~~~~~~~~~~~~~~~~~~~~~

Contains commands for running tests in the local environment
"""
import os

import sys
import subprocess
from lettuce.bin import main as run_lettuce
from flask.ext.script import Command


class RunTest(Command):  # pragma: no cover
    """Runs tests"""

    def __init__(self, kind):
        self.kind = kind
        self.module_name = 'tests.{0}'.format(self.kind)

    def get_arguments(self):
        return [
            '--immediate',
            '--with-coverage',
            '--cover-branches',
            '--cover-erase',
            '--cover-package=bong.api',
            '--cover-package=bong.security',
            '--cover-package=bong.framework',
            '--cover-min-percentage=100%',
            '--nologcapture',
            '--rednose',
            '--logging-clear-handlers',
            '--stop',
            '--verbosity=2',
            '--stop',
            'tests/{0}'.format(self.kind),
        ]

    def run(self):
        os.environ['TESTING'] = 'true'
        if self.kind == 'unit':
            os.environ['UNIT_TESTING'] = 'true'

        print "Scanning for {0} tests".format(self.kind)
        code = subprocess.call(['nosetests'] + self.get_arguments())
        sys.exit(code)


class RunAcceptanceTests(Command):  # pragma: no cover
    """Runs lettuce tests"""

    def run(self):
        run_lettuce(sys.argv[2:])
