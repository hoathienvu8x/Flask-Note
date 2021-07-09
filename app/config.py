# -*- coding: utf-8 -*-

import os

class Config(object):
    DEBUG = False
    TESTING = False

class Configuration(Config):
    ENV = "development"
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    PORT = 9800
