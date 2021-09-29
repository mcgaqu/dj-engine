# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Biz

#------------------------
# Biz
#------------------------
class BizSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Biz
        fields = ['url', 'id', 'alias', 'name']
        
 

class BizViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Biz.objects.all().order_by('alias')
    serializer_class = BizSerializer
