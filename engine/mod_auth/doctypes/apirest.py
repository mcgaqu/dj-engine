# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import DocType, DocTypeProp


#--------------------------
# DocType
#-------------------------
class DocTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocType
        fields = ['url', 'id', 'company', 'alias', 'name']
        
 

class DocTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = DocType.objects.all().order_by('alias')
    serializer_class = DocTypeSerializer


class DocTypePropSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocTypeProp
        fields = ['url', 'id', 'doctype', 'alias', 'name']
        
 

class DocTypePropViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = DocTypeProp.objects.all().order_by('doctype', 'alias')
    serializer_class = DocTypePropSerializer


