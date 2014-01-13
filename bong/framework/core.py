#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <Copyright 2013 - Gabriel Falcão <gabriel@weedlabs.io>>

from __future__ import unicode_literals

# python stuff
import os
import sys

# 3rd party stuff
from flask import Flask, render_template
from flask.ext.script import Manager

# our stuff
from bong import settings

from . import log
from .http.assets import AssetsManager
from .http.sessions import RedisSessionInterface


class Application(object):
    """

    Welcome to the Bong Application!
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This class is the backbone of the Bong application: it knows
    how to bootstrap a new flask app and enable various features like
    command line interface, assets, session, logging and so on.
    """
    testing_mode = settings.TESTING

    def __init__(self, settings_path='bong.settings', *args, **kwargs):
        self.assets = None
        self.commands_manager = None
        self.flask_app = Flask(__name__, *args, **kwargs)
        self.flask_app.config.from_object(settings_path)

    def enable_error_handlers(self):
        """Enables the http error handlers (404, 500, etc) to default
        ones defined inline in this method.

        They basically render `templates/{statuscode}.html`
        """
        handler_for = ErrorHandlers(self.flask_app)

        # Enabling the handler for status 500 - internal server error
        self.add_error_handler(500, handler_for.internal_error)

    def add_error_handler(self, status_code, callback):
        handler = self.flask_app.errorhandler(status_code)
        return handler(callback)

    def __call__(self, *args, **kw):
        """Making this class behave like a WSGI app, forwarding the
        call to flask"""
        return self.flask_app(*args, **kw)

    def enable_session(self, session_interface=None):
        """Uses redis as session interface"""
        self.flask_app.session_interface = session_interface or RedisSessionInterface()

    def enable_assets(self):
        """Enable support to WebAssets:
        http://elsdoerfer.name/docs/flask-assets/
        """
        self.assets = AssetsManager(self.flask_app)

    def enable_commands(self, commands):
        """Takes a list of 2-item tuples containing a command label
        for the shell and the command instance.

        This command both sets up the commands structure and register
        the given commands.
        """
        # Ensure local mode
        os.environ.setdefault("BONG_LOCAL_MODE", "true")

        # preparing the command manager
        self.commands_manager = Manager(self.flask_app)

        if self.assets:  # enabling the assets command
            self.assets.create_assets_command(self.commands_manager)

        # registering each given command
        for label, command in commands:
            self.commands_manager.add_command(label, command)

    def run_cli(self):
        """Runs the command line interface"""
        if not self.commands_manager:
            raise RuntimeError('The method run_cli can only be called '
                               'after the `enable_commands` method was called.')

        self.commands_manager.run()

    def register_blueprint(self, bp):
        """Simple method proxy to flask_app.register_blueprint()
        """
        return self.flask_app.register_blueprint(bp)

    def setup_logging(self, output, level):
        """Takes a file descriptor, log level and a list of logger
        names.

        Adds a StreamHandler pointing to the given output for each
        given logger.

        Also sets all the loggers to the given level.
        """
        if self.testing_mode:
            # don't register loggers if in testing_mode
            return

        loggers = [self.flask_app.logger]
        for name in settings.LOGGER_NAMES:
            logger = log.get_logger(name)
            self.setup_handler_for_logger(logger, output, level)

        return loggers

    def setup_handler_for_logger(self, logger, output, level):
        handler = log.get_pretty_log_handler(output)
        logger.addHandler(handler)
        logger.setLevel(level)
        return logger

    @classmethod
    def from_env(CreateApplication,
                 environment_variable_name='BONG_SETTINGS_MODULE',
                 fallback_module_name='bong.settings',
                 *flask_args,
                 **flask_kwargs
        ):
        """Returns an instance of `Application` fed with settings from
        the env + centralizes all the plugins and blueprint setup.

        This method is supposed to set up the flask app with
        everything we need for production.

        If the code is related to the setup of the flask app in the
        local environment (i.e: commands) it doesn't belong here.
        """

        settings_module = os.environ.get(
            environment_variable_name,  # 'BONG_SETTINGS_MODULE'
            fallback_module_name,       # 'bong.settings'
        )

        # Creating the application, now we can enable portions of the
        # flask_app separately, abstracted in methods to organize the
        # code and make it 100% testable.
        application = CreateApplication(settings_module, *flask_args, **flask_kwargs)

        # HTTP Error handling: making sure the app will render nice
        # 403, 404, 500... pages
        application.enable_error_handlers()

        return application


class ErrorHandlers(object):
    def __init__(self, flask_app):
        self.flask_app = flask_app

    def internal_error(self, exception):
        self.flask_app.logger.exception("The Flask application suffered an internal error")
        return render_template('500.html', exception=exception), 500
