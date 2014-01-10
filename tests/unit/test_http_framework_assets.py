#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals
from mock import patch, Mock
from bong.framework.http.assets import AssetsManager


@patch('bong.framework.http.assets.Environment')
def test_assets_manager(Environment):
    ("AssetsManager should have a flask assets Environment "
     "setup upon instantiation")

    # Background: the assets environment is mocked
    assets_environment = Environment.return_value
    # And it returns a fake folder for get_directory
    assets_environment.get_directory.return_value = '/fake/dir'
    # And the load_path is an empty list
    assets_environment.load_path = []

    # Given a fake app instance
    app = Mock()

    # When I instantiate the AssetsManager with that app
    manager = AssetsManager(app)

    # Then the manager should have an Environment
    manager.should.have.property('env').being.equal(Environment.return_value)

    # And the load_path of the Environment should be the one returned by get_directory
    assets_environment.load_path.should.equal(['/fake/dir'])

    # And set_directory should have been called with None
    assets_environment.set_directory.assert_called_once_with(None)
