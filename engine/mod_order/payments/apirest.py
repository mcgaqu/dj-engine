# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Payment, PaymentAux



#------------------------
# Payment
#------------------------
class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'url', 'name']
        
 

class PaymentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Payment.objects.all() # .order_by('name')
    serializer_class = PaymentSerializer

#------------------------
# PaymentAux
#------------------------
class PaymentAuxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaymentAux
        fields = ['id', 'url', 'name']
        
 

class PaymentAuxViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = PaymentAux.objects.all() # .order_by('name')
    serializer_class = PaymentAuxSerializer
