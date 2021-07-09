# -*- coding: utf-8 -*-

from app import engine
from flask import Response, jsonify, request
from .endpoint import get_handler

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

    key = "{}_api".format(endpoint)
    handle = get_handler(key)

    if handle is None:
        return jsonify({
            "error":"Endpoint '{}' is not defined.".format(endpoint)
        })

    retVal = handle(request)

    return jsonify(retVal)

@engine.route("/api/remove", methods=["GET","POST"])
@engine.route("/api/<string:endpoint>/remove", methods=["GET","POST"])
def remove_node(endpoint=""):
    endpoint = endpoint.strip()
    if not endpoint:
        if request.method == "POST":
            if request.content_type and ("application/json" in request.content_type):
                req = request.get_json()
            else:
                req = request.form
        elif request.method == "GET":
            req = request.args

        endpoint = req.get("endpoint","").strip()
        if not endpoint:
            return jsonify({
                "error":"Command is not valid."
            })

    key = "{}_remove".format(endpoint)
    handle = get_handler(key)

    if handle is None:
        return jsonify({
            "error":"Endpoint '{}' is not defined.".format(endpoint)
        })

    retVal = handle(request)

    return jsonify(retVal)
