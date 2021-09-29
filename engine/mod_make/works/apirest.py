# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Work, WorkAux



#------------------------
# Work
#------------------------
class WorkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Work
        fields = ['id', 'url', 'name']
        
 

class WorkViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Work.objects.all() # .order_by('name')
    serializer_class = WorkSerializer

#------------------------
# WorkAux
#------------------------
class WorkAuxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkAux
        fields = ['id', 'url', 'name']
        
 

class WorkAuxViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = WorkAux.objects.all() # .order_by('name')
    serializer_class = WorkAuxSerializer
