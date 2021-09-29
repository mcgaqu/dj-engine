# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Delivery, DeliveryAux



#------------------------
# Delivery
#------------------------
class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'url', 'name']
        
 

class DeliveryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Delivery.objects.all() # .order_by('name')
    serializer_class = DeliverySerializer

#------------------------
# DeliveryAux
#------------------------
class DeliveryAuxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeliveryAux
        fields = ['id', 'url', 'name']
        
 

class DeliveryAuxViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = DeliveryAux.objects.all() # .order_by('name')
    serializer_class = DeliveryAuxSerializer
