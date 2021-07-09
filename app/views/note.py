# -*- coding: utf-8 -*-

from app import engine
from flask import Response

@engine.route("/")
def root_node():
    return 'Health check good.'

@engine.route("/api")
@engine.route("/api/")
def api_node():
    return Response(
        response='Command is not valid',
        status=403,
        mimetype='text/plain'
    )
