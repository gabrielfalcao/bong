#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import logging
from bong import settings
from datetime import datetime


class ColorFormatter(logging.Formatter):  # pragma: no cover
    # prints a nice output colored by log level
    COLORS = {
        'DEBUG': '\033[37m',
        'INFO': '\033[32m',
        'ERROR': '\033[1;31m',
        'WARNING': '\033[32m',
        'CRITICAL': '\033[35m',
        'FATAL': '\033[36m',
    }

    def format(self, record):
        level_name = record.levelname.upper()
        original = logging.Formatter.format(self, record)
        color = self.COLORS.get(level_name, '\033[37m')
        time = datetime.now().strftime("\033[37m[%Y-%m-%d %H:%M:%S]\033[0m")
        msg = "{time} {color}[{level_name}]\033[1;37m {original}\033[0m"
        return msg.format(**locals())


def get_pretty_log_handler(write_filedescriptor):  # pragma: no cover
    formatter = ColorFormatter()
    handler = logging.StreamHandler(write_filedescriptor)
    handler.setFormatter(formatter)

    if settings.TESTING:
        handler = logging.NullHandler()

    return handler


def get_logger(name='bong'):  # pragma: no cover
    if settings.TESTING:
        from mock import Mock
        return Mock(name=name)

    if name.split('.')[0] not in settings.LOGGER_NAMES:
        msg = ("bong.log.get_logger requested a "
               "logger name that is not registered "
               "in settings.LOGGER_NAMES, you might "
               "want to fix it somehow: {0}\n")
        sys.stderr.write(msg.format(name))
    return logging.getLogger(name)

DEFAULT_LOGGERS = []
for name in settings.LOGGER_NAMES:
    DEFAULT_LOGGERS.append(get_logger(name))
