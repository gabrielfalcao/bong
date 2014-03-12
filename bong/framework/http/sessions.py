#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@weedlabs.io>
#
from __future__ import unicode_literals
import pickle
from datetime import timedelta
from uuid import uuid4
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from bong.framework.db import get_redis_connection


# disabling test coverage here for now because we don't need assets yet.

class RedisSession(CallbackDict, SessionMixin):  # pragma: no cover
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(SessionInterface):  # pragma: no cover
    serializer = pickle
    session_class = RedisSession

    def __init__(self, prefix='bong:http:sessid',  redis=None):
        if redis is None:
            redis = get_redis_connection(db=2)

        self.redis = redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def make_key(self, sid):
        return ":".join([self.prefix, sid])

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)

        key = self.make_key(sid)
        val = self.redis.get(key)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)

        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        session_id = session.sid
        cookie_name = app.session_cookie_name

        cookie_expiration = self.get_expiration_time(app, session)
        redis_expiration = self.get_redis_expiration_time(app, session)

        domain = self.get_cookie_domain(app)
        if not session:
            key = self.make_key(session_id)
            self.redis.delete(key)
            if session.modified:
                response.delete_cookie(cookie_name,
                                       domain=domain)
            return

        value = self.serializer.dumps(dict(session))

        key = self.make_key(session_id)
        expiration = int(redis_expiration.total_seconds())
        self.redis.setex(key, expiration, value)

        response.set_cookie(cookie_name, session_id,
                            httponly=True,
                            domain=domain,
                            expires=cookie_expiration)
