# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

engine = Flask("app")

from .config import Configuration

engine.config.from_object(Configuration)

db = SQLAlchemy(engine,session_options={"autoflush": False})

from .views import *
