# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Invoice, InvoiceAux



#------------------------
# Invoice
#------------------------
class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'url', 'name']
        
 

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Invoice.objects.all() # .order_by('name')
    serializer_class = InvoiceSerializer

#------------------------
# InvoiceAux
#------------------------
class InvoiceAuxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvoiceAux
        fields = ['id', 'url', 'name']
        
 

class InvoiceAuxViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = InvoiceAux.objects.all() # .order_by('name')
    serializer_class = InvoiceAuxSerializer
