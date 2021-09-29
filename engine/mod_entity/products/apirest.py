# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Category, Product, ProductAux

#------------------------
# Category
#------------------------
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'url', 'name']
        
 

class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Category.objects.all() # .order_by('name')
    serializer_class = CategorySerializer


#------------------------
# Product
#------------------------
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'url', 'name']
        
 

class ProductViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Product.objects.all() # .order_by('name')
    serializer_class = ProductSerializer

#------------------------
# ProductAux
#------------------------
class ProductAuxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductAux
        fields = ['id', 'url', 'name']
        
 

class ProductAuxViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = ProductAux.objects.all() # .order_by('name')
    serializer_class = ProductAuxSerializer
