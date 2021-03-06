# -*- coding: utf-8 -*-

import os

class Config(object):
    DEBUG = False
    TESTING = False

SQLALCHEMY_DATABASE_PATH = "{}".format(os.path.join(os.path.dirname(os.path.realpath(__file__)),"data"))

class Configuration(Config):
    ENV = "development"
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    MINIFY_HTML = True

    CACHE_TYPE = "simple"

    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(SQLALCHEMY_DATABASE_PATH, "notes.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    PORT = 9800
