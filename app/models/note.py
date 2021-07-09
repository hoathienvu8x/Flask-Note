# -*- coding: utf-8 -*-

from app import db
from datetime import datetime

class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, nullable=False, default='', index=True, unique=True)
    content = db.Column(db.Text, nullable=False, default='')
    status = db.Column(db.String(10), nullable=False, default='pending')
    url = db.Column(db.String(128), nullable=True)
    name = db.Column(db.String(128), nullable=True)
    views = db.Column(db.Integer, default=0, nullable=True)
    publish = db.Column(db.DateTime, nullable=False, default=datetime(1970, 1, 1))
    modified = db.Column(db.DateTime, nullable=False, default=datetime(1970, 1, 1))

    def __init__(self):
        pass

    def __repr__(self):
        return "<Note#{}/>".format(self.id)
