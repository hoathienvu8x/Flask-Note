# -*- coding: utf-8 -*-

from app import engine, cache, API_KEY
from flask import render_template, abort, request, redirect, url_for
from .endpoint import _note_query_handle, _note_recents_handle, \
_note_hits_handle, _note_api_handle, _note_remove_handle
from .note import _get_request

def get_list_pages(page, pages):
    start = page - 2
    if start <= 0:
        start = 1

    end = start + 4
    if end > pages:
        end = pages

    if end - start < 4:
        start = end - 4
        if start <= 0:
            start = 1

    return {
        "start": start,
        "page": page,
        "end": end,
        "pages": pages
    }

@engine.route("/graph/")
@engine.route("/graph/page/<int:page>/")
@cache.memoize(20)
def gui_node(page=1):
    argv = {
        "site_title": "Simple Flask Note"
    }
    if page <= 0:
        page = 1
    limit = 10
    args = {
        "page": str(page),
        "limit": str(limit),
        "fields":"node,content,name,url,timestamp",
        "key":API_KEY
    }
    if request.args.get("s","").strip():
        args["action"] = "search"
        args["s"] = request.args.get("s","").strip()

    retVal = _note_query_handle(args)
    navi = None
    if "total_pages" in retVal:
        if retVal["total_pages"] > 1:
            navi = get_list_pages(retVal["page"], retVal["total_pages"])

    argv["navi"] = navi
    argv["page"] = page
    argv["notes"] = retVal["data"] if "data" in retVal else None
    argv["endpoint"] = "notes"
    return render_template('note.html', **argv)

@engine.route("/graph/recents/")
@engine.route("/graph/recents/page/<int:page>/")
@cache.memoize(20)
def gui_recent_node(page=1):
    argv = {
        "site_title": "Simple Flask Note"
    }
    if page <= 0:
        page = 1
    limit = 10
    retVal = _note_recents_handle({
        "page": str(page),
        "limit": str(limit),
        "fields":"node,content,name,url,timestamp",
        "key":API_KEY
    })
    navi = None
    if "total_pages" in retVal:
        if retVal["total_pages"] > 1:
            navi = get_list_pages(restVal["page"], retVal["total_pages"])

    argv["navi"] = navi
    argv["page"] = page
    argv["notes"] = retVal["data"] if "data" in retVal else None
    argv["endpoint"] = "recents"
    return render_template('note.html', **argv)

@engine.route("/graph/hits/")
@engine.route("/graph/hits/page/<int:page>/")
@cache.memoize(20)
def gui_hit_node(page=1):
    argv = {
        "site_title": "Simple Flask Note"
    }
    if page <= 0:
        page = 1
    limit = 10
    retVal = _note_hits_handle({
        "page": str(page),
        "limit": str(limit),
        "fields":"node,content,name,url,timestamp",
        "key":API_KEY
    })
    navi = None
    if "total_pages" in retVal:
        if retVal["total_pages"] > 1:
            navi = get_list_pages(restVal["page"], retVal["total_pages"])

    argv["navi"] = navi
    argv["page"] = page
    argv["notes"] = retVal["data"] if "data" in retVal else None
    argv["endpoint"] = "hits"
    return render_template('note.html', **argv)

@engine.route("/note/<string:node>/")
@cache.memoize(60)
def gui_detail_node(node=''):
    node = node.strip()
    if not node:
        abort(404)
    retVal = _note_query_handle({
        "node":node,
        "fields":"node,content,name,url,timestamp",
        "key":API_KEY
    })
    argv = {
        "site_title": "Simple Flask Note"
    }
    if "error" in retVal:
        argv["site_title"] = "Error"
        argv["message"] = retVal["error"]
    else:
        argv["note"] = retVal["data"]
        if "name" in retVal["data"] and retVal["data"]["name"].strip():
            argv["site_title"] = retVal["data"]["name"]

    return render_template('note.html', **argv)

@engine.route("/graph/new", methods=["GET","POST"])
def gui_new_node():
    args = _get_request(request)
    retVal = _note_api_handle(args)
    argv = {
        "site_title": "Simple Flask Note"
    }
    if "error" in retVal:
        argv["site_title"] = "Error"
        argv["message"] = retVal["error"]
    else:
        return redirect(url_for(".gui_detail_node", node=retVal["data"]["node"]))

    return render_template('note.html', **argv)

@engine.route("/graph/remove/<string:node>")
def gui_remove_node(node=''):
    node = node.strip()
    if not node:
        abort(404)

    args = _get_request(request)
    from .endpoint import _note_check_api_key
    retVal = _note_check_api_key(args)
    if retVal is None:
        retVal = _note_remove_handle({
            "node" : node
        })
    if "error" in retVal:
        argv["site_title"] = "Error"
        argv["message"] = retVal["error"]
    else:
        return redirect(url_for(".gui_node", removed="done"))

    return render_template('note.html', **argv)
