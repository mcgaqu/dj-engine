# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework import serializers, generics, viewsets, filters
from .models import User, Group

from mod_admin.utils.base import get_apirest_fields

#----------------------------
# Idea para personaliza apis : --> Pendiente de prueba y mejora.
#--------------------------

def x_get_api_fields(Model, ini_fields=[]):
    from mod_bpmn.data.models import BModelField
    if settings.NUM_ADMIN_SITE == '2':
        fields = BModelField.objects.filter(
            bmodel__biz__name=settings.SITE_NAME, name=Model.__name__)
        return [x.alias for x in fields]
    return ini_fields


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = ['url', 'id', 'username', 'email']
        # fields = get_api_fields(model, ['url', 'id', 'username', 'email'])
        fields = get_apirest_fields(User)

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    search_fields = ['alias', 'name']
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'url', 'name']
        fields = get_apirest_fields(Group)
        # fields = '__all__'



class GroupViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer