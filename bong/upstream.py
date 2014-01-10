#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

from socketio.sgunicorn import GeventSocketIOWorker as BaseWorker


nonflash_transports = [
    'xhr-polling',
    'htmlfile',
    'xhr-multipart',
    'xhr-polling',
    'jsonp-polling',
]

websocket_transports = nonflash_transports + ['websocket']


class WebsocketsSocketIOWorker(BaseWorker):
    """Good for nginx > 1.4"""
    transports = websocket_transports


class NonFlashSocketIOWorker(BaseWorker):
    """This one is just for upstream http servers that don't support
    websockets"""
    transports = nonflash_transports
