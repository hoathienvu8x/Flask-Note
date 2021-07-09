# -*- coding: utf-8 -*-

from app import engine
from flask import Response, jsonify, request

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

@engine.route("/api/<string:endpoint>", methods=["GET","POST"])
def endpoint_node(endpoint=""):
    endpoint = endpoint.strip()
    if not endpoint:
        return jsonify({
            "error":"Command is not valid."
        })

    from .endpoint import get_handler

    key = "{}_api".format(endpoint)
    handle = get_handler(key)

    if handle is None:
        return jsonify({
            "error":"Endpoint '{}' is not defined.".format(endpoint)
        })

    retVal = handle(request)

    return jsonify(retVal)
