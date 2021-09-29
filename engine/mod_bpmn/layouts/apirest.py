# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Component, CompProp  #, Layout

#------------------------
# Component
#------------------------
class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = ['url', 'id', 'biz', 'alias', 'name']
        
 

class ComponentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Component.objects.all().order_by('alias')
    serializer_class = ComponentSerializer


class CompPropSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompProp
        fields = ['url', 'id', 'component', 'component_id', 'alias', 'name']
        
 

class CompPropViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = CompProp.objects.all().order_by('component', 'alias')
    serializer_class = CompPropSerializer

