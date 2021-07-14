# -*- coding: utf-8 -*-

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .note import Note

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    Notes = SQLAlchemyConnectionField(Note)

schemas = graphene.Schema(query=Query)