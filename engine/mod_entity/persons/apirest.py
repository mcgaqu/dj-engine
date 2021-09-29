# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from rest_framework import filters
# from django_filters.rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# from django_filters.rest_framework.filters import OrderingFilter


# from .models import NeodCliente, NeodClienteContacto
from .models import Segment, Customer


#------------------------
# Segment
#------------------------
class SegmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Segment
        fields = ['id', 'url', # 'doctype_id', 'doctype',
        'alias', 'name', 'active'
        ] 
 

class SegmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Segment.objects.all() # .order_by('name')
    serializer_class = SegmentSerializer




#------------------------
# Customer
#------------------------
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'url', 'alias', 'name', 
            'active', 'sort', # (DNI)
            'doctype_id', 
            'first_name', 'last_name', 'avatar',
            'address', 'stateAbbr', 'city', 'zipcode',
            'birthday',
        ]
        
 

class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all() # .order_by('last_name')
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, 
                        filters.SearchFilter,
                        filters.OrderingFilter]
    filterset_fields = ['stateAbbr', 'sort', 'active']
    search_fields = ['alias', 'name', 'city'] # , 'typedoc__name'
    ordering_fields = ['alias', 'name', 'city']
    ordering = ['name']






"""
#------------------------
# NeodCliente
#------------------------
class NeodClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NeodCliente
        fields = '__all__'
        
 

class NeodClienteViewSet(viewsets.ModelViewSet):

    queryset = NeodCliente.objects.all().order_by('cod_trabajo')
    serializer_class = NeodClienteSerializer


#--------------------------
# NeodClienteContacto
#-------------------------
class NeodClienteContactoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NeodClienteContacto
        fields = '__all__'
        
 

class NeodClienteContactoViewSet(viewsets.ModelViewSet):
 
    queryset = NeodClienteContacto.objects.all().order_by('codigo')
    serializer_class = NeodClienteContactoSerializer

"""