# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from rest_framework import filters
# from django_filters.rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, CompanyLoad, CompanyProp, Menu, MenuItem

from mod_admin.utils.base import get_apirest_fields
#--------------------------
# Company
#-------------------------
class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        # fields = ['url', 'id', 'alias', 'name']
        fields = get_apirest_fields(Company)
 

class CompanyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Company.objects.all().order_by('alias')
    serializer_class = CompanySerializer
    # filter_backends = [DjangoFilterBackend, 
    #                     filters.SearchFilter,
    #                     filters.OrderingFilter]
    # filterset_fields = []
    search_fields = ['alias', 'name'] # , 'typedoc__name'
    ordering_fields = ['alias', 'name']
    ordering = ['alias']
    # pagination_class = PageNumberPagination


class CompanyLoadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompanyLoad
        # fields = ['url', 'id', 'company', 'company_id', 'alias', 'name']
        fields = get_apirest_fields(CompanyLoad)       
 

class CompanyLoadViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = CompanyLoad.objects.all().order_by('company', 'alias')
    serializer_class = CompanyLoadSerializer
    # filter_backends = [DjangoFilterBackend, 
    #                     filters.SearchFilter,
    #                     filters.OrderingFilter]
    filterset_fields = ['company']
    search_fields = ['alias', 'name'] # , 'typedoc__name'
    ordering_fields = ['alias', 'name']
    ordering = ['alias']
    # pagination_class = PageNumberPagination

#---------------------------
class CompanyPropSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompanyProp
        # fields = ['url', 'id', 'company', 'company_id', 'alias', 'name']
        fields = get_apirest_fields(CompanyProp)       
 

class CompanyPropViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = CompanyProp.objects.all().order_by('company', 'alias')
    serializer_class = CompanyPropSerializer
    # filter_backends = [DjangoFilterBackend, 
    #                     filters.SearchFilter,
    #                     filters.OrderingFilter]
    filterset_fields = ['company']
    search_fields = ['alias', 'name'] # , 'typedoc__name'
    ordering_fields = ['alias', 'name']
    ordering = ['alias']
    # pagination_class = PageNumberPagination
#--------------------------
# Menu
#-------------------------
class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        # fields = ['url', 'id',  'alias', 'name', 'note']
        fields = get_apirest_fields(Menu)       
 

class MenuViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Menu.objects.all().order_by('alias')
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, 
                        filters.SearchFilter,
                        filters.OrderingFilter]
    # filterset_fields = ['cod_delegacion', 'articulo', 'fec_modif']
    search_fields = ['alias', 'name', 'note'] # , 'typedoc__name'
    ordering_fields = ['id', 'alias', 'name']
    ordering = ['alias']
    # pagination_class = PageNumberPagination



class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MenuItem
        # fields = ['url', 'id',  'alias', 'name', 'menu', 'menu_id']
        fields = get_apirest_fields(MenuItem)       
 

class MenuItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = MenuItem.objects.all().order_by('menu', 'alias')
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, 
                        filters.SearchFilter,
                        filters.OrderingFilter]
    # filterset_fields = ['cod_delegacion', 'articulo', 'fec_modif']
    search_fields = ['alias', 'name'] # , 'typedoc__name'
    ordering_fields = ['menu', 'alias', 'name']
    ordering = ['menu']
    # pagination_class = PageNumberPagination

