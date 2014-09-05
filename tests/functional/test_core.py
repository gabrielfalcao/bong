#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@nacaolivre.org>
#
from __future__ import unicode_literals
import sys
import logging
from plant import Node
from mock import MagicMock
from StringIO import StringIO
from flask import Blueprint
from bong.server import application
from bong.framework.core import Application
from bong.framework.core import ErrorHandlers
from bong.framework.commands.testing import RunTest

this_file = Node(__file__)
this_folder = this_file.parent


def test_enabling_all_application_features_should_work():
    ("Enabling all application features should work")

    app = Application.from_env()
    app.testing_mode = False
    app.enable_session()
    app.enable_assets()
    app.enable_commands([('test', RunTest('*'))])

    app.setup_logging(sys.stderr, 0)
    app.commands_manager = MagicMock()
    app.run_cli()


    test = Blueprint('test-all', __name__)
    @test.route('/path/to', methods=['GET'])
    def handle_path():
        return 'COOL!'

    app.register_blueprint(test)

    environ = {
        'SERVER_NAME': 'testserver',
        'SERVER_PORT': '8080',
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/path/to',
        'wsgi.url_scheme': 'http://',
    }
    wsgi = MagicMock(name='WSGIMock')
    result = '\n'.join(list(app(environ, wsgi)))
    result.should.equal('COOL!')


def test_run_cli_without_enabling_commands_beforehand():
    ("Trying to run the cli without having called "
     "enable_commands() beforehand should raise RuntimeError "
     "with a meaningful message")

    app = Application.from_env()
    app.run_cli.when.called.should.throw(
        RuntimeError,
        'The method run_cli can only be called after the `enable_commands` method was called.',
    )


def test_setup_logging_in_test_mode():
    ("Calling Application.setup_logging while in testing mode should't do anything")

    # Given an output
    output = StringIO()

    # And an Application
    app = Application.from_env()
    app.testing_mode = True
    app.enable_commands([])

    # When I setup_logging with the given output
    app.setup_logging(output, 0)

    # And do some logging
    app.flask_app.logger.info("LOGGING WORKS FINE :)")

    # Then the output should be empty
    output.getvalue().should.be.empty


def test_error_handler_internal_error():
    ("ErrorHandlers.internal_error should render a 500 template and return 500 status")

    output = StringIO()
    # Given a valid app
    app = application.flask_app
    application.testing_mode = False
    application.setup_logging(output, logging.INFO)
    application.testing_mode = True

    # And a valid ErrorHandlers instance
    errors = ErrorHandlers(app)

    # And a valid exception
    boom = ValueError('HELLO')

    # When I call internal_error on that exception
    with app.test_request_context('/oops'):
        app.logger.info('Just a friendly notification that I am about to test how the application tests for errors:')
        body, status = errors.internal_error(boom)
        app.logger.info('All good again :)')

    # Then it should have returned status 500
    status.should.equal(500)

    # And the template should have rendered appropriately
    body.should.contain('Hypertext Transfer Protocol -- HTTP/1.1')
