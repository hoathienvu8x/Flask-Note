# -*- coding: utf-8 -*-

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..models.note import Note as NoteModel

class Note(SQLAlchemyObjectType):
    class Meta:
        model = NoteModel
        interfaces = (graphene.relay.Node, )

    slug = graphene.String(name="node")