#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

import bcrypt
import sqlalchemy as db

from bong import settings
from bong.framework.db import Model, metadata
from bong.framework.log import get_logger

from bong.framework.handy.functions import now


logger = get_logger('bong.web.models')


class User(Model):
    table = db.Table(
        'user', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('email', db.String(100), nullable=False, unique=True),
        db.Column('password', db.String(128), nullable=False),
        db.Column('created_at', db.DateTime, default=now),
    )

    def to_dict(self):
        data = self.to_dict_original()
        data.pop('password')
        return data

    @classmethod
    def authenticate(cls, email, password):
        user = cls.find_one_by(email=email)

        if not user:
            return

        if user.password == cls.secretify_password(password):
            return user

    @classmethod
    def secretify_password(cls, plain):
        salt = 'pr0p3l'
        salted = salt.join(str(plain))
        return bcrypt.hashpw(salted, settings.SALT)

    @classmethod
    def create(cls, email, password):
        password = cls.secretify_password(password)
        return super(User, cls).create(email=email, password=password)
