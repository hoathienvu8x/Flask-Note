# -*- coding: utf-8 -*-

import hashlib, re
from app import db
from datetime import datetime, timedelta
from ..models.note import Note

def content_hash(content=""):
    m = hashlib.md5()
    m.update(content.encode())
    return m.hexdigest()

def _no_accent(s):
    specials = ["&amp;","&lt;","&gt;","&lsquo;","&rsquo;","&ldquo;","&rdquo;","&hellip;","&ndash;","&mdash;","&quot;","&#39;","&nbsp;","&#91;","&#93;","&#32;"]
    for i in range(len(specials)):
        s = re.sub(specials[i],' ', s)
    return s

def _the_short_content(s, length=160):
    s = _no_accent(s)
    s = re.sub(r'[\W_]+', ' ', s)
    s = re.sub(r' +',r' ',s)
    s = s.strip()
    if len(s) <= length:
        return s

    _length = len(s)
    words = s.split(" ")
    s = ""
    for word in words:
        word = word.strip()
        if word:
            s += word + " "
            if len(s.strip()) >= length:
                if len(s) < _length:
                    return s.strip() + "..."

    return s

def _note_custom_dict(note, fields, short=False):
    item = {}
    for i in range(len(fields)):
        k = fields[i]
        if k == "slug" or k == "node":
            item["node"] = note.slug
        elif k == "timestamp":
            item[k] = str(note.modified).replace(" ","T") if note.modified > note.publish else str(note.publish).replace(" ","T")
        elif hasattr(note, k):
            item[k] = getattr(note,k)
            if k == "modified" and note.modified < note.publish:
                item[k] = None
            if k == "modified" or k == "publish":
                if item[k] is not None:
                    item[k] = str(item[k]).replace(" ","T")
            elif k == "content":
                if short == True:
                    item[k] = _the_short_content(s=item[k])

    return item

def _get_note_optional_args(args):
    if args.get("fields","").strip():
        fields = [ v for v in args.get("fields","").strip().split(",") if v.strip() ]
    else:
        fields = ["node", "content", "status", "timestamp"]

    page = args.get("page","1").strip()
    if not page:
        page = "1"

    try:
        page = int(page)
        if page <= 0:
            page = 1
    except:
        page = 1

    limit = args.get("limit","5").strip()
    if not limit:
        limit = "5"

    try:
        limit = int(limit)
        if limit <= 0:
            limit = 5
    except:
        limit = 5

    state = args.get("state","").strip()
    if state:
        state = state.lower()
        if not (state in ["all","publish","pending","draft","trash"]):
            state = "publish"
    else:
        state = "all"

    return (page, limit, state, fields)

def _note_api_handle(args=None):
    if args is None:
        return {
            "data":[]
        }

    id = args.get("id", "").strip()
    content = args.get("content","").strip()
    status = args.get("status","").strip()
    url = args.get("url","").strip()
    name = args.get("name","").strip()

    if not content:
        return {
            "error": "Content is empty."
        }

    if id:
        try:
            id = int(id)
        except:
            id = -1
        if id <= 0:
            return {
                "error":"Note is not exists."
            }
    else:
        id = -1

    if id > 0:
        note = Note.query.get(id)
        if note is None:
            return {
                "error":"Note is not exists."
            }
    else:
        digest = content_hash(content)
        note = Note.query.filter(Note.slug.ilike("{}_%".format(digest))).first()
        if not bool(note):
            note = Note()

    if note.content != content:
        note.content = content
        if note.id is None:
            note.publish = datetime.now()
        else:
            note.modified = datetime.now()

    status = status.lower()
    if status in ["publish", "pending", "draft", "trash"]:
        note.status = status
    if ("http://" in url or "https://" in url) and note.url != url:
        note.url = url
    if name:
        note.name = name

    if note.slug is None:
        digest = content_hash(note.content)
        note.slug = "{}_{}".format(digest,int(datetime.timestamp(note.publish)))
        db.session.add(note)

    try:
        db.session.commit()
        return {
            "data": _note_custom_dict(note, ["node", "content", "status", "timestamp"])
        }
    except Exception as e:
        db.session.rollback()
        return {
            "error":"Could not {} note, error: \"{}\"".format("update" if id > 0 else "add", e)
        }

def _note_remove_handle(args=None):
    if args is None:
        return {
            "data":[]
        }

    if args.get("id","").strip():
        id = args.get("id",-1, int)
        if id <= 0:
            return {
                "error":"ID ({}) is not valid".format(id)
            }
        note = Note.query.get(id)
        if note is None:
            return {
                "error": "Note is not exists"
            }
        node = note.slug
        db.session.delete(note)
        try:
            db.session.commit()
            return {
                "message":"Note node '{}' removed".format(node)
            }
        except Exception as e:
            db.session.rollback()
            return {
                "error":"Could not remove note node '{}', error: \"{}\"".format(node,e),
            }

    node = args.get("node","").strip()
    if not node:
        return {
            "error":"Node is not valid"
        }
        
    note = Note.query.filter(Note.slug == node).first()
    if not bool(note):
        return {
            "error": "Note node '{}' is not exists".format(node)
        }
    db.session.delete(note)
    try:
        db.session.commit()
        return {
            "message":"Note node '{}' removed".format(node)
        }
    except Exception as e:
        db.session.rollback()
        return {
            "error":"Could not remove note node '{}', error: \"{}\"".format(node, e),
        }

def _note_query_handle(args=None):
    if args is None:
        return {
            "data":[]
        }

    action = args.get("action","get").strip()
    if not action:
        action = "get"
    action = action.lower()
    if not (action in ["get","search"]):
        action = "get"

    page, limit, state, fields = _get_note_optional_args(args)

    if action == "search":
        keyword = args.get("s","").strip()
        if not keyword:
            return {
                "error":"Keyword is required"
            }

        query = Note.query.filter(Note.content.ilike("%{}%".format(keyword)))
        if state != "all":
            query = query.filter(Note.status == state)

        query = query.order_by(Note.publish.desc()).paginate(page, limit, error_out=False)
        return {
            "num_results" : len(query.items),
            "data":[ _note_custom_dict(note, fields, True) for note in query.items ],
            "page" : query.page,
            "total_pages" : query.pages
        }

    node = args.get("node","").strip()
    if node:
        note = Note.query.filter(Note.slug == node).first()
        if not bool(note):
            return {
                "error" : "Note is not exists"
            }

        views = note.views + 1 if note.views is not None else 1
        note.views = views

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        return {
            "data":_note_custom_dict(note, fields)
        }

    query = Note.query
    if state != "all":
        query = query.filter(Note.status == state)

    query = query.order_by(Note.publish.desc()).paginate(page, limit, error_out=False)
    return {
        "num_results" : len(query.items),
        "data":[ _note_custom_dict(note,fields, True) for note in query.items ],
        "page" : query.page,
        "total_pages" : query.pages
    }

def _note_recents_handle(args=None):
    if args is None:
        return {
            "data":[]
        }

    page, limit, state, fields = _get_note_optional_args(args)

    since = datetime.now() - timedelta(hours=24)
    query = Note.query.filter(Note.publish >= since)
    if state != "all":
        query = query.filter(Note.status == state)

    query = query.order_by(Note.publish.desc()).paginate(page, limit, error_out=False)
    return {
        "num_results" : len(query.items),
        "data":[ _note_custom_dict(note,fields, True) for note in query.items ],
        "page" : query.page,
        "total_pages" : query.pages
    }

def _note_hits_handle(args=None):
    if args is None:
        return {
            "data":[]
        }

    page, limit, state, fields = _get_note_optional_args(args)

    query = Note.query.filter(Note.views > 0)
    if state != "all":
        query = query.filter(Note.status == state)

    query = query.order_by(Note.views.desc()).paginate(page, limit, error_out=False)
    return {
        "num_results" : len(query.items),
        "data":[ _note_custom_dict(note,fields, True) for note in query.items ],
        "page" : query.page,
        "total_pages" : query.pages
    }

endpoints = {
    "note_api" : _note_api_handle,
    "note_remove" : _note_remove_handle,
    "note_query" : _note_query_handle,
    "note_recents" : _note_recents_handle,
    "note_hits" : _note_hits_handle
}

def get_handler(key=''):
    key = key.strip()
    if not key:
        return None
    if not (key in endpoints):
        return None
    return endpoints[key]
