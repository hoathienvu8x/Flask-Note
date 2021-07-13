# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_htmlmin import HTMLMIN
from flask_caching import Cache

engine = Flask("app")

from .config import Configuration

engine.config.from_object(Configuration)

db = SQLAlchemy(engine,session_options={"autoflush": False})
htmlmin = HTMLMIN(engine)
cache = Cache(engine)

API_KEY = ""

from .views import *
