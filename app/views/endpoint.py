# -*- coding: utf-8 -*-

import hashlib
from app import db
from datetime import datetime
from ..models.note import Note

def content_hash(content=""):
    m = hashlib.md5()
    m.update(content.encode())
    return m.hexdigest()

def _note_api_handle(request=None):
    if request is None:
        return {
            "data":[]
        }

    if request.method == "POST":
        if request.content_type and ("application/json" in request.content_type):
            req = request.get_json()
        else:
            req = request.form
    elif request.method == "GET":
        req = request.args

    id = req.get("id", "").strip()
    content = req.get("content","").strip()
    status = req.get("status","").strip()
    url = req.get("url","").strip()
    name = req.get("name","").strip()

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
            "data": {
                "node": note.slug,
                "content":note.content,
                "status":note.status,
                "timestamp": str(note.modified).replace(" ","T") if note.modified > note.publish else str(note.publish).replace(" ","T")
            }
        }
    except Exception as e:
        db.session.rollback()
        return {
            "error":"Could not {} note, error: \"{}\"".format("update" if id > 0 else "add", e)
        }

endpoints = {
    "note_api" : _note_api_handle
}

def get_handler(key=''):
    key = key.strip()
    if not key:
        return None
    if not (key in endpoints):
        return None
    return endpoints[key]
