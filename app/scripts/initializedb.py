# -*- coding: utf-8 -*-

from ..models.note import Note

def init_database(db):
    db.drop_all()
    db.create_all()
