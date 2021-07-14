# -*- coding: utf-8 -*-

from app import engine
from flask_graphql import GraphQLView
from ..gql.schema import schemas

engine.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schemas,
        graphiql=True
    )
)