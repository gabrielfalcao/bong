#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
from __future__ import unicode_literals, absolute_import

"""
bong.commands.db
~~~~~~~~~~~~~~~~~~~~~~

Contains commands for handling db stuff in the local environment
"""

import os
from flask.ext.script import Command


class CreateDB(Command):  # pragma: no cover
    def __init__(self, application):
        self.application = application

    def run(self, dbname='bong'):
        print "Creating database `bong`"
        os.system("echo 'drop database if exists {0}' | mysql -uroot 2>&1 >> makedb.log".format(dbname))
        os.system("echo 'create database {0}' | mysql -uroot 2>&1 >> makedb.log".format(dbname))
        print "Running migrations"
        os.system('alembic -c alembic.ini upgrade head 2>&1 >> makedb.log')
