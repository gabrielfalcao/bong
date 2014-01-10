#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals
import logging
from mock import patch, Mock, call
from bong.framework.core import Application, ErrorHandlers


@patch('bong.framework.core.Flask')
def test_application_has_flask_app(Flask):
    ("Application should contain a flask app")

    # Given a settings import path
    test_path = 'path.to.test.settings'

    # When I create an application with that path
    app = Application(test_path)

    # Then a flask app must have been created
    Flask.assert_called_once_with('bong.framework.core')

    # And the flask app instance must be available as `flask_app`
    # inside of the Application instance
    app.flask_app.should.equal(Flask.return_value)


@patch('bong.framework.core.ErrorHandlers')
@patch('bong.framework.core.Flask')
def test_application_enable_error_handlers(Flask, ErrorHandlers):
    ("Application.enable_error_handlers() should register a error handler for 500")

    # Given an application that mocks `add_error_handler`
    class MyApplication(Application):
        add_error_handler = Mock(name='MyApplication.add_error_handler')

    app = MyApplication()

    # When I enable error handling
    app.enable_error_handlers()

    # Then an instance of ErrorHandlers has been created
    handler_for = ErrorHandlers.return_value

    # And the handler for internal server error must have been added
    app.add_error_handler(500, handler_for.internal_error)


@patch('bong.framework.core.Flask')
def test_add_error_handler(Flask):
    ("Application.add_error_handler registers flask error "
     "handler for the given status code and callback")

    # Given an application
    app = Application()

    # And a callback
    def callback(): pass

    # When I add that callback as an error handler
    app.add_error_handler(403, callback)

    # Then an error handler decorator must have been created
    app.flask_app.errorhandler.assert_called_once_with(403)

    # And the handler was used for decorating the callback
    handler = app.flask_app.errorhandler.return_value
    handler.assert_called_once_with(callback)


@patch('bong.framework.core.Flask')
def test_application_must_be_callable(Flask):
    ("Application must be callable and forward the call to the flask app")

    # Given an application
    app = Application()

    # When I call it
    result = app('some', arguments=True)

    # Then the result must have come from the flask app
    result.should.equal(Flask.return_value.return_value)

    # And it should have been called with the given arguments
    app.flask_app.assert_called_once_with('some', arguments=True)


@patch('bong.framework.core.RedisSessionInterface')
@patch('bong.framework.core.Flask')
def test_application_enable_session(Flask, RedisSessionInterface):
    ("Application.enable_session() should set the session_interface "
     "to be the RedisSessionInterface")

    # Given an application
    app = Application()

    # When I enable session
    app.enable_session()

    # Then the session interface of the flask app should be RedisSessionInterface()
    app.flask_app.session_interface.should.equal(RedisSessionInterface.return_value)


@patch('bong.framework.core.Flask')
def test_application_enable_session_with_custom_interface(Flask):
    ("Application.enable_session() should can take the session interface as argument")

    # Given an application
    app = Application()

    # And a mock of Flask Session Interface
    session_interface = Mock(name='MockSessionInterface')

    # When I enable session
    app.enable_session(session_interface)

    # Then the session interface of the flask app should be the given session_interface
    app.flask_app.session_interface.should.equal(session_interface)



@patch('bong.framework.core.AssetsManager')
@patch('bong.framework.core.Flask')
def test_application_enable_assets(Flask, AssetsManager):
    ("Application.enable_assets() should instantiate an AssetsManager and create the bundles")

    # Given an application
    app = Application()

    # When I enable assets
    app.enable_assets()

    # Then the assets manager should have been instantiated
    app.assets.should.equal(AssetsManager.return_value)

    # And `create_bundles` should have been called
    app.assets.create_bundles.assert_called_once_with()



@patch('bong.framework.core.Manager')
@patch('bong.framework.core.Flask')
def test_application_enable_commands(Flask, Manager):
    ("Application.enable_commands() should take a list of "
     "tuples containing a label and a command instance")

    # Given an application
    app = Application()

    # And a fake command
    command1 = Mock()

    # When I enable commands passing the given command
    app.enable_commands([('label1', command1)])

    # Then the commands_manager should have been set appropriately
    app.commands_manager.should.equal(Manager.return_value)

    # And the command should have been added with the given label
    app.commands_manager.add_command.assert_called_once_with('label1', command1)


@patch('bong.framework.core.Manager')
@patch('bong.framework.core.Flask')
def test_application_enable_commands_after_enabling_assets(Flask, Manager):
    ("Application.enable_commands() should take a list of "
     "tuples containing a label and a command instance")

    # Given an application that has mocked assets
    app = Application()
    app.assets = Mock(name='FakeAssets')

    # And a fake command
    command1 = Mock()

    # When I enable commands passing the given command
    app.enable_commands([('label1', command1)])

    # Then the asset commands should have been enabled
    app.assets.create_assets_command.assert_called_once_with(app.commands_manager)

    # And the command should have been added with the given label
    app.commands_manager.add_command.assert_called_once_with('label1', command1)


@patch('bong.framework.core.Flask')
def test_application_register_blueprint(Flask):
    ("Application.register_blueprint() should add the blueprint to the main app")

    # Given an application
    app = Application()

    # And a blueprint mock
    blueprint = Mock(name='FakeBluePrint')

    # When I register the blueprint
    app.register_blueprint(blueprint)

    # Then it should have been registered within the flask app
    app.flask_app.register_blueprint.assert_called_once_with(blueprint)


@patch('bong.framework.core.Flask')
def test_application_run_cli_without_commands(Flask):
    ("Application.run_cli() should raise a RuntimeError "
     "if the commands weren't enabled previously")

    # Given an application
    app = Application()

    # When I run cli
    call_to_run_cli = app.run_cli.when.called

    # Then it should have raised a descriptive RuntimeError
    call_to_run_cli.should.throw(RuntimeError,
                                 'The method run_cli can only be called '
                                 'after the `enable_commands` method was called.')


@patch('bong.framework.core.Flask')
def test_application_run_cli(Flask):
    ("Application.run_cli() should run the commands managers")

    # Given an application that has a commands_manager
    app = Application()
    app.commands_manager = Mock(name='FakeCommandsManager')

    # When I run cli
    app.run_cli()

    # Then it should run the commands_manager
    app.commands_manager.run.assert_called_once_with()


@patch('bong.framework.core.log')
@patch('bong.framework.core.Flask')
def test_setup_handler_for_logger(Flask, log):
    ("Application.setup_handler_for_logger should add a pretty handler "
     "and set the level to the given level")

    # Given an application that has a commands_manager
    app = Application()

    # And a fake logger
    logger = Mock(name='FakeLogger')

    # And a fake output
    output = Mock(name='FakeFileObject')

    # When I call setup_handler_for_logger
    result = app.setup_handler_for_logger(logger, output, logging.INFO)

    # Then it should get the pretty handler for the given output
    log.get_pretty_log_handler.assert_called_once_with(output)
    handler = log.get_pretty_log_handler.return_value

    # And the handler should have been added to the logger
    logger.addHandler.assert_called_once_with(handler)

    # And the level of the logger should be set to the given logging level
    logger.setLevel.assert_called_once_with(logging.INFO)


@patch('bong.framework.core.Flask')
def test_setup_logging_does_nothing_in_test_mode(Flask):
    ("Application.setup_logging does nothing when in testing mode")

    # Given an application in test mode
    app = Application()
    app.testing_mode = True

    # And an output
    output = Mock(name='FakeFileObject')

    # Then running it will just return None
    app.setup_logging(output, 'Any Level').should.be.none


@patch('bong.framework.core.log')
@patch('bong.framework.core.Flask')
def test_setup_logging(Flask, log):
    ("Application.setup_logging sets up")

    # Background: log.get_logger will return the given name
    log.get_logger.side_effect = lambda x: 'handler for [{0}]'.format(x)

    # Given an application not in testing mode that mocks the
    # setup_handler_for_logger method
    class MyApplication(Application):
        setup_handler_for_logger = Mock(name='MyApplication.setup_handler_for_logger')

    app = MyApplication()
    app.testing_mode = False

    # And an output
    output = Mock(name='FakeFileObject')

    # When I setup logging
    loggers = app.setup_logging(output, logging.WARNING)

    # Then a logger should have been retrieved for each name in the settings file
    log.get_logger.assert_has_calls([
        call('bong'),
        call('bong.api.models'),
        call('bong.api.resources'),
        call('bong.framework.http'),
        call('bong.framework.db'),
    ])

    # And setup_handler_for_logger should have been called for each handler
    app.setup_handler_for_logger.assert_has_calls([
        call('handler for [bong]', output, logging.WARNING),
        call('handler for [bong.api.models]', output, logging.WARNING),
        call('handler for [bong.api.resources]', output, logging.WARNING),
        call('handler for [bong.framework.http]', output, logging.WARNING),
        call('handler for [bong.framework.db]', output, logging.WARNING),

   ])


@patch('bong.framework.core.os')
@patch('bong.framework.core.RedisSessionInterface')
@patch('bong.framework.core.Flask')
def test_from_env(Flask, RedisSessionInterface, os):
    ("Application.from_env should create app from environment variable")

    # Background: Given an application that mocks out
    # `enable_error_handlers` and `enable_session`
    class MyApplication(Application):
        enable_error_handlers = Mock(name='MyApplication.enable_error_handlers')

    # Given an environment variable name that points to a settings python path
    environment_variable = 'PROJECTNAME_SETTINGS_MODULE'

    # And a fallback module name
    fallback_module_name = 'projectname.settings'

    # When I call from_env giving those attributes
    app = MyApplication.from_env(environment_variable, fallback_module_name)

    # Then it should retrieve the variable from the system
    os.environ.get.assert_called_once_with('PROJECTNAME_SETTINGS_MODULE', 'projectname.settings')

    # And the application should have been created from the given settings
    app.flask_app.config.from_object.assert_called_once_with(os.environ.get.return_value)

    # And the error handlers should have been enabled
    app.enable_error_handlers.assert_called_once_with()


@patch('bong.framework.core.render_template')
def test_error_handlers_internal_error(render_template):
    ("ErrorHandlers.internal_error should take an exception and "
     "render the 500 template passing `exception` to the context")

    # Given a fake flask app
    flask_app = Mock(name='FakeFlaskApp')

    # And an instance of ErrorHandlers
    handler_for = ErrorHandlers(flask_app)

    # And a synthesized exception
    exception = RuntimeError('BOOM')

    # When I call internal_error with that exception
    result = handler_for.internal_error(exception)

    # Then it should have returned a tuple with the result from `render_template` and the status code 500
    result.should.be.a(tuple)
    result.should.equal((render_template.return_value, 500))

    # And the render_template should have been called appropriately
    render_template.assert_called_once_with('500.html', exception=exception)

    # And the exception should have been logged
    flask_app.logger.exception.assert_called_once_with('The Flask application suffered an internal error')
