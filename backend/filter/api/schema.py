import graphene
from .resolvers import FilterQuery

class Query(FilterQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query) 