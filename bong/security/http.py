#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals

from flask import request
from functools import wraps

from bong.framework.http import JSONResource, json_response
from bong.api.models import User
from bong.api.roles import PublicRole

from . import FilterRegistry, RoleRegistry


def forbidden(description):
    return json_response({'error': 'Forbidden', 'description': description}, 403)


def get_authenticated_user(given_role_names=None):
    if given_role_names is None:
        given_role_names = RoleRegistry.keys()

    token = request.headers.get('X-Bong-Token', '')
    if not token:
        return None, forbidden('Missing X-Bong-Token')

    user = User.from_token(token)
    if not user:
        return None, forbidden('Invalid X-Bong-Token')

    if not user.roles.match_any(given_role_names):
        return None, forbidden('Access Denied for User Roles')

    return user, None


def allow_roles(*given_role_names):
    from bong import settings

    def decorate(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not settings.UNIT_TESTING:  # pragma: no cover
                user, response = get_authenticated_user(given_role_names)
                if not user:
                    return response

            return f(*args, **kwargs)

        return decorated_function

    return decorate


class RoleJSONResource(JSONResource):
    @property
    def user(self):
        user, response = get_authenticated_user()
        return user

    def role_filter(self, model):
        if not self.user:
            role = PublicRole
        else:
            role = self.user.role
        wrapper = FilterRegistry.for_model_and_role(role, model)
        return wrapper(model)

    def dispatch_request(self, *args, **kwargs):
        response = super(RoleJSONResource, self).dispatch_request(*args, **kwargs)
        just_options = request.method.upper() == 'OPTIONS'
        if just_options:
            return response

        return response
