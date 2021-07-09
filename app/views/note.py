# -*- coding: utf-8 -*-

from app import engine

@engine.route("/")
def root_node():
    return 'Health check good.'
