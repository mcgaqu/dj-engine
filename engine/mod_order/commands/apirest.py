# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Command, CommandAux



#------------------------
# Command
#------------------------
class CommandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Command
        fields = ['id', 'url', 'name']
        
 

class CommandViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Command.objects.all() # .order_by('name')
    serializer_class = CommandSerializer

#------------------------
# CommandAux
#------------------------
class CommandAuxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommandAux
        fields = ['id', 'url', 'name']
        
 

class CommandAuxViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = CommandAux.objects.all() # .order_by('name')
    serializer_class = CommandAuxSerializer
