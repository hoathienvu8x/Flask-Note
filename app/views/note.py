# -*- coding: utf-8 -*-

from app import engine, cache
from flask import Response, jsonify, request
from .endpoint import get_handler

def _get_request(request=None):
    if request is None:
        return None
    if request.method == "POST":
        if request.content_type and ("application/json" in request.content_type):
            req = request.get_json()
        else:
            req = request.form
    elif request.method == "GET":
        req = request.args
    return req

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

    args = _get_request(request)

    retVal = handle(args)

    return jsonify(retVal)

@engine.route("/api/remove", methods=["GET","POST"])
@engine.route("/api/<string:endpoint>/remove", methods=["GET","POST"])
def remove_node(endpoint=""):
    endpoint = endpoint.strip()
    if not endpoint:
        args = _get_request(request)

        endpoint = args.get("endpoint","").strip()
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

    args = _get_request(request)

    retVal = handle(args)

    return jsonify(retVal)

@engine.route("/api/query", methods=["GET","POST"])
@engine.route("/api/<string:endpoint>/query", methods=["GET","POST"])
@cache.memoize(20)
def query_node(endpoint=""):
    endpoint = endpoint.strip()
    if not endpoint:
        args = _get_request(request)

        endpoint = args.get("endpoint","").strip()
        if not endpoint:
            return jsonify({
                "error":"Command is not valid."
            })

    key = "{}_query".format(endpoint)
    handle = get_handler(key)

    if handle is None:
        return jsonify({
            "error":"Endpoint '{}' is not defined.".format(endpoint)
        })

    args = _get_request(request)

    retVal = handle(args)

    return jsonify(retVal)

@engine.route("/api/recents", methods=["GET","POST"])
@engine.route("/api/<string:endpoint>/recents", methods=["GET","POST"])
@cache.memoize(20)
def recent_node(endpoint=""):
    endpoint = endpoint.strip()
    if not endpoint:
        args = _get_request(request)

        endpoint = args.get("endpoint","").strip()
        if not endpoint:
            return jsonify({
                "error":"Command is not valid."
            })

    key = "{}_recents".format(endpoint)
    handle = get_handler(key)

    if handle is None:
        return jsonify({
            "error":"Endpoint '{}' is not defined.".format(endpoint)
        })

    args = _get_request(request)

    retVal = handle(args)

    return jsonify(retVal)

@engine.route("/api/hits", methods=["GET","POST"])
@engine.route("/api/<string:endpoint>/hits", methods=["GET","POST"])
@cache.memoize(20)
def hit_node(endpoint=""):
    endpoint = endpoint.strip()
    if not endpoint:
        args = _get_request(request)

        endpoint = args.get("endpoint","").strip()
        if not endpoint:
            return jsonify({
                "error":"Command is not valid."
            })

    key = "{}_hits".format(endpoint)
    handle = get_handler(key)

    if handle is None:
        return jsonify({
            "error":"Endpoint '{}' is not defined.".format(endpoint)
        })

    args = _get_request(request)

    retVal = handle(args)

    return jsonify(retVal)
