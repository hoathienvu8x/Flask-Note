# -*- coding: utf-8 -*-

from app import engine
import markdown
from flask import Markup
from .endpoint import _the_short_content
from .figure import FigureCaption

@engine.context_processor
def the_jinja_content():
    return dict(the_excerpt=_the_short_content)

@engine.template_filter("the_time")
def the_time(d):
    from datetime import datetime
    import math
    now = datetime.timestamp(datetime.now())
    if isinstance(d,str):
        try:
            d = d.split(".")[0]
            d = datetime.strptime(d,"%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            print(e)
            return d

    seconds = datetime.timestamp(d)
    sec = int(now - seconds)
    if sec <= 5:
        return "Just now"

    hours = math.floor(sec / 3600)
    if hours == 0:
        mins = math.floor(sec / 60)
        if mins == 0:
            return "{} seconds ago".format(sec)
        else:
            return "{} minutes ago".format(mins)
    elif hours < 24:
        return "{} hours ago".format(hours)
    return d.strftime("%d/%m/%Y @%H:%M")

@engine.context_processor
def inject_now():
    from datetime import datetime
    return {'now': datetime.utcnow()}

@engine.template_filter('markdown')
def neomarkdown(markdown_content):
    return Markup(markdown.markdown(markdown_content, extensions=['tables','codehilite','fenced_code',FigureCaption()]))
