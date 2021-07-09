# -*- coding: utf-8 -*-

from app import engine
from flask import Response, jsonify

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
            "error":"Command is not valid.",
            "data":None
        })

    return jsonify({
        "data":[]
    })
