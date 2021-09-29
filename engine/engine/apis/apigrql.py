# -*- coding: utf-8 -*-
"""
import graphene

from graphene_django.debug import DjangoDebug

from mod_auth.adjango.apigql import Query as AuthdjangoQuery, Mutation as AuthdjamgoMutation



class Query(
    AuthdjangoQuery,
    # PersonsQuery, 
    graphene.ObjectType):
    # debug = graphene.Field(DjangoDebug, name="_debug")
    pass

class Mutation(
    AuthdjamgoMutation,
    graphene.ObjectType):
    pass

# schema = graphene.Schema(query=Query, mutation=Mutation)
schema = graphene.Schema(query=Query, mutation=Mutation)

"""