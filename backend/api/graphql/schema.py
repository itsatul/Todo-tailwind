"""
Main GraphQL schema for Todo app.
"""

import graphene
from .queries import Query
from .mutations import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation) 