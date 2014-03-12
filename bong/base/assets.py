#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# flake8: noqa

from __future__ import unicode_literals

from flask.ext.assets import (
    Bundle,
)

jquery = Bundle('vendor/jquery/jquery.js')
angular = Bundle(
    'vendor/angular/angular.js',
    'vendor/angular-ui-router/release/angular-ui-router.js',
    'vendor/angular-local-storage/angular-local-storage.js',
)

bootstrap_js = Bundle(
    "vendor/bootstrap/dist/js/bootstrap.js"
)

bootstrap_css = Bundle(
    # # Core variables and mixins
    "vendor/bootstrap/less/variables.less",
    "vendor/bootstrap/less/mixins.less",

    # # # Reset
    # "vendor/bootstrap/less/normalize.less",
    # "vendor/bootstrap/less/print.less",

    # # Core CSS
    "vendor/bootstrap/less/scaffolding.less",
    # "vendor/bootstrap/less/type.less",
    # "vendor/bootstrap/less/code.less",
    # "vendor/bootstrap/less/grid.less",
    # "vendor/bootstrap/less/tables.less",
    # "vendor/bootstrap/less/forms.less",
    # "vendor/bootstrap/less/buttons.less",

    # # # # Components
    # "vendor/bootstrap/less/component-animations.less",
    # "vendor/bootstrap/less/glyphicons.less",
    # "vendor/bootstrap/less/dropdowns.less",
    # "vendor/bootstrap/less/button-groups.less",
    # "vendor/bootstrap/less/input-groups.less",
    # "vendor/bootstrap/less/navs.less",
    # "vendor/bootstrap/less/navbar.less",
    # "vendor/bootstrap/less/breadcrumbs.less",
    # "vendor/bootstrap/less/pagination.less",
    # "vendor/bootstrap/less/pager.less",
    # "vendor/bootstrap/less/labels.less",
    # "vendor/bootstrap/less/badges.less",
    # "vendor/bootstrap/less/jumbotron.less",
    # "vendor/bootstrap/less/thumbnails.less",
    # "vendor/bootstrap/less/alerts.less",
    # "vendor/bootstrap/less/progress-bars.less",
    # "vendor/bootstrap/less/media.less",
    # "vendor/bootstrap/less/list-group.less",
    # "vendor/bootstrap/less/panels.less",
    # "vendor/bootstrap/less/wells.less",
    # "vendor/bootstrap/less/close.less",

    # # # # Components w/ JavaScript
    # "vendor/bootstrap/less/modals.less",
    # "vendor/bootstrap/less/tooltip.less",
    # "vendor/bootstrap/less/popovers.less",
    # "vendor/bootstrap/less/carousel.less",

    # # # # Utility classes
    # "vendor/bootstrap/less/utilities.less",
    # "vendor/bootstrap/less/responsive-utilities.less",
    # "vendor/bootstrap/less/responsive-utilities.less",
    # "less/bootswatch.less",

    filters=('recess',),
)
