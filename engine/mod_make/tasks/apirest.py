# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Task, TaskAux



#------------------------
# Task
#------------------------
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'url', 'name']
        
 

class TaskViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Task.objects.all() # .order_by('name')
    serializer_class = TaskSerializer

#------------------------
# TaskAux
#------------------------
class TaskAuxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskAux
        fields = ['id', 'url', 'name']
        
 

class TaskAuxViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = TaskAux.objects.all() # .order_by('name')
    serializer_class = TaskAuxSerializer
