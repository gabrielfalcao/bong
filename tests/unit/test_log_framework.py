#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@nacaolivre.org>
#
from __future__ import unicode_literals
from mock import patch, Mock
from bong.framework.log import (
    ColorFormatter,
    get_pretty_log_handler,
    get_logger,
)


@patch('bong.framework.log.settings')
@patch('bong.framework.log.logging')
def test_get_logger(logging, settings):
    ("log.get_logger should be a simple proxy to logging.getLogger")
    settings.TESTING = False

    # Given I call get logger
    logger = get_logger('somename')

    # When it should be the result from logging.getLogger
    logger.should.equal(logging.getLogger.return_value)



@patch('bong.framework.log.settings')
@patch('bong.framework.log.logging')
@patch('bong.framework.log.ColorFormatter')
def test_get_pretty_log_handler(ColorFormatter, logging, settings):
    ("get_pretty_log_handler takes a file descriptor and "
     "returns a log handler that uses the ColorFormatter")
    settings.TESTING = False

    # Given a fake file descriptor
    output = Mock()

    # When I call get_pretty_log_handler
    handler = get_pretty_log_handler(output)

    # Then it should have returned a stream handler
    handler.should.equal(logging.StreamHandler.return_value)

    # And the StreamHandler should have been constructed with the
    # given file descriptor
    logging.StreamHandler.assert_called_once_with(output)

    # And the handler got the formatter set to be the ColorFormatter
    handler.setFormatter.assert_called_once_with(ColorFormatter.return_value)


def test_color_formatter_colors():
    ("ColorFormatter should have an ANSI color table for the given levels")

    ColorFormatter.COLORS.should.have.key('DEBUG').being.equal('\033[37m')
    ColorFormatter.COLORS.should.have.key('INFO').being.equal('\033[32m')
    ColorFormatter.COLORS.should.have.key('ERROR').being.equal('\033[1;31m')
    ColorFormatter.COLORS.should.have.key('WARNING').being.equal('\033[32m')
    ColorFormatter.COLORS.should.have.key('CRITICAL').being.equal('\033[35m')
    ColorFormatter.COLORS.should.have.key('FATAL').being.equal('\033[36m')


@patch('bong.framework.log.logging')
@patch('bong.framework.log.datetime')
def test_color_formatter_format(datetime, logging):
    ("ColorFormatter.format when formatting was successful should "
     "get the color for the level name and format with time")

    logging.Formatter.format.return_value = 'THE LOG MESSAGE'
    datetime.now.return_value.strftime.return_value = '[NICE-FORMATTED-DATE]'
    # Given a mocked record object
    record = Mock()
    record.levelname = 'critical'

    # And an instance of the ColorFormatter
    formatter = ColorFormatter()

    # When I call format on my fake record
    result = formatter.format(record)

    # Then it should have returned the expected
    result.should.equal('[NICE-FORMATTED-DATE] \x1b[35m[CRITICAL]\x1b[1;37m THE LOG MESSAGE\x1b[0m')

    # And the super() for format should have been called appropriately
    logging.Formatter.format.assert_called_once_with(formatter, record)

    # And strftime should have been called appropriately
    datetime.now.return_value.strftime.assert_called_once_with("\033[37m[%Y-%m-%d %H:%M:%S]\033[0m")
