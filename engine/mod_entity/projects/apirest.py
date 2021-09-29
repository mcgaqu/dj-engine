# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Project, Expedient, ExpedientAux

#------------------------
# Project
#------------------------
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'url', 'name']
        
 

class ProjectViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Project.objects.all() # .order_by('name')
    serializer_class = ProjectSerializer


#------------------------
# Expedient
#------------------------
class ExpedientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Expedient
        fields = ['id', 'url', 'name']
        
 

class ExpedientViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Expedient.objects.all() # .order_by('name')
    serializer_class = ExpedientSerializer

#------------------------
# ExpedientAux
#------------------------
class ExpedientAuxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExpedientAux
        fields = ['id', 'url', 'name']
        
 

class ExpedientAuxViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = ExpedientAux.objects.all() # .order_by('name')
    serializer_class = ExpedientAuxSerializer
