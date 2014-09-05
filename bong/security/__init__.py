#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@nacaolivre.org>
#
from __future__ import unicode_literals


class RoleRegistry(object):
    _registry = {}

    @classmethod
    def keys(cls):
        return cls._registry.keys()

    @classmethod
    def get_by_name(self, name):
        return self._registry.get(name)

    @classmethod
    def clear(self):
        return self._registry.clear()

    @classmethod
    def register_role(cls, label, Role):
        cls._registry[label] = Role

    @classmethod
    def highest_within(self, role_names=[]):
        roles = filter(bool, [self._registry.get(r) for r in role_names])
        roles = sorted(roles, key=lambda r: r.weight, reverse=True)
        if roles:
            return roles[0].label

        return None


class RoleMeta(type):
    def __init__(cls, name, bases, attrs):
        if name == 'Role':
            return

        exception_message = (
            "The role class {0}.{1} doesn't define the attribute `{2}`")

        for required in ['label', 'weight']:
            if not hasattr(cls, required):
                msg = exception_message.format(cls.__module__, name, required)
                raise InvalidRoleDeclaration(msg)

        RoleRegistry.register_role(cls.label, cls)
        super(RoleMeta, cls).__init__(name, bases, attrs)


class Role(object):
    __metaclass__ = RoleMeta


class InvalidRoleDeclaration(Exception):
    pass


class InvalidFilterDeclaration(Exception):
    pass


class FilterRegistry(object):
    __registry = {}

    @classmethod
    def register_filter(cls, filtr):
        registry = cls.__registry
        registry[(filtr.role, filtr.model)] = filtr

    @classmethod
    def for_model_and_role(cls, role, model_instance):
        registry = cls.__registry
        return registry[(role, model_instance.__class__)]


class FilterMeta(type):
    def __init__(cls, name, bases, attrs):
        if name == 'RoleFilter':
            return

        exception_message = (
            "The role filter class {0}.{1} doesn't define the attribute `{2}`")

        if not hasattr(cls, 'role'):
            msg = exception_message.format(cls.__module__, name, 'role')
            raise InvalidFilterDeclaration(msg)

        if not hasattr(cls, 'model'):
            msg = exception_message.format(cls.__module__, name, 'model')
            raise InvalidFilterDeclaration(msg)

        FilterRegistry.register_filter(cls)
        super(FilterMeta, cls).__init__(name, bases, attrs)


class RoleFilter(object):
    __metaclass__ = FilterMeta

    def __init__(self, model):
        self.model = model

    def only_the_keys(self, dictionary, allowed_keys):
        return dict([(key, value) for key, value in dictionary.items() if key in allowed_keys])

    def but_the_keys(self, dictionary, forbidden_keys):
        return dict([(key, value) for key, value in dictionary.items() if key not in forbidden_keys])
