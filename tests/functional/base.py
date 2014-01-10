#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals

import sqlalchemy as db

from datetime import datetime

from sure import scenario
from freezegun import freeze_time

from bong.server import application
from bong.framework.db import metadata, engine, Model, get_redis_connection


time_frozen = freeze_time("2002-04-20 04:20:00")


class User(Model):
    table = db.Table('md_user', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('github_id', db.Integer, nullable=False, unique=True),
        db.Column('github_token', db.String(256), nullable=True),
        db.Column('gravatar_id', db.String(40), nullable=False, unique=True),
        db.Column('username', db.String(80), nullable=False, unique=True),
        db.Column('email', db.String(100), nullable=False, unique=True),
        db.Column('created_at', db.DateTime, default=datetime.now),
        db.Column('updated_at', db.DateTime, default=datetime.now),
    )


@time_frozen
def prepare_app(context):
    context.http = application.flask_app.test_client()


def prepare_db(context):
    conn = engine.connect()
    metadata.drop_all(engine)
    metadata.create_all(engine)
    context.redis = get_redis_connection(15)
    context.redis.flushdb()
    context.frozen_datetime = datetime(2002, 4, 20, 4, 20)

specification = scenario([prepare_app, prepare_db])

def api_specification(role_name, email='foo@bar.com', password='123'):
    from bong.api.models import User
    def prepare_token(context):
        context.user = User.create(email=email, password=password)
        context.user.created_at = datetime(2002, 4, 20, 4, 20)
        context.user.save()
        context.user.roles.add(role_name)
        context.token = context.user.generate_token()
        context.headers = {'X-Bong-Token': context.token}

    return scenario([prepare_app, prepare_db, prepare_token])
