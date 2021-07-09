# -*- coding: utf-8 -*-

import os
from flask import Flask

engine = Flask("app")

from .config import Configuration

engine.config.from_object(Configuration)

from .views import *
