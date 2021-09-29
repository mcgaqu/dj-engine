# -*- coding: utf-8 -*-
from rest_framework import serializers, generics, viewsets
from .models import Folder, FolderAnnex


#--------------------------
# Folder
#-------------------------
class FolderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Folder
        fields = ['url', 'id',
            'doctype','grade', 'sort', 'alias', 'name', 'mark', 'docfile', 'content',
            'active', 'locked', 'MH_content'
        ]
        
 

class FolderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Folder.objects.all().order_by('sort')
    serializer_class = FolderSerializer
    filterset_fields = ['grade', 'sort', 'mark', 'active', 'locked']
    search_fields = ['alias', 'name'] # , 'typedoc__name'
    ordering_fields = ['grade', 'sort', 'mark', 'alias', 'name']
    ordering = ['sort']


class FolderAnnexSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FolderAnnex
        fields = ['url', 'id', 'folder', 'alias', 'name']
        
 

class FolderAnnexViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = FolderAnnex.objects.all().order_by('folder', 'alias')
    serializer_class = FolderAnnexSerializer

    # filterset_fields = []
    search_fields = ['alias', 'name'] # , 'typedoc__name'
    ordering_fields = ['alias', 'name']
    ordering = ['alias']
