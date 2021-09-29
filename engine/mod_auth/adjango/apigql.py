# -*- coding: utf-8 -*-
"""
import graphene
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import User, Group
Node = relay.Node

class GroupNode(DjangoObjectType):
    class Meta:
        model = Group
        interfaces = (Node,)
        filter_fields = ["name", # "users"
        ]
        # fields = []  '__all__'
        # exclude = []
    
    
    # CAMPOS CALCULADOS
    # campox = graphene.String()
    # def resolve_campox(self, info):
    #    return "Hola"

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)
        filter_fields = ["username", "groups"]

    # @classmethod
    # def get_queryset(cls, queryset, info):
    #     if info.context.user.is_anonymous:
    #         return queryset.filter(active=True)
    #     return queryset

class Query(object):
    group = Node.Field(GroupNode)
    all_groups = DjangoFilterConnectionField(GroupNode)

    user = Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)


#============================================

class CreateGroupMutation(graphene.Mutation):
    class Input:
        name = graphene.String()
    
    name = graphene.Field(GroupNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        name = kwargs.get('name', '').strip()
        obj = Group.objects.create(name=name)
        return CreateGroupMutation(name=obj)

class CreateUserMutation(graphene.Mutation):
    class Input(object):
        username = graphene.String()
        first_name = graphene.String()
        email = graphene.String()
    
    name = graphene.Field(UserNode)
  
    @staticmethod
    def mutate(root, info, **kwargs):
        username = kwargs.get('username', '').strip()
        first_name = kwargs.get('first_name', '').strip()
        email = kwargs.get('email', '').strip()
        # category_id = kwargs.get('category_id', 0)
        obj = User.objects.create(username=username,first_namer=first_name,
                email=email)
        return CreateUserMutation(name=obj)


class Mutation(graphene.AbstractType):
    create_group = CreateGroupMutation.Field()
    create_user = CreateUserMutation.Field()

"""

