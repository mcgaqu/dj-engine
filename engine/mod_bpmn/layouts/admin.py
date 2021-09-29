# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
from .models import Component, CompProp, Layout 




class CompPropLin1(ModelLin1):
    model = CompProp
    fields = ['sort', 'alias', 'name', 'json', 'active'] # 'name', 'grade', 'sort']

class CompPropAdmin1(ModelAuxAdmin1):
    model = CompProp
    list_display = ['MC_grade', 'component', 'alias', 'name', 'json', 'grade', 'sort']
    list_filter = ['component__grade', 'component',  'active']
    search_fields = ['component__alias', 'component__name']
    fields = ['alias', 'name', 'json', 'grade', 'sort']



class ComponentAdmin1(ModelAdmin1):
    model = Component
    list_display = ['biz', 'alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    list_filter = ['biz', 'active', 'grade']
    inlines = [CompPropLin1]

#-----------------------

class LayoutChildLin1(ModelLin1):
    model = Layout
    fk_name = 'parent'
    fields = ['sort', 'alias', 'comp', 'active'] # 'name', 'grade', 'sort']


class LayoutAdmin1(ModelAdmin1):
    model = Layout
    list_display = ['biz', 'level','parent', 'alias', 'name', 'comp', 'grade', 'sort']
    fields = [('alias', 'name', 'grade', 'sort', 'comp')]
    list_filter = ['level', 'grade']
    inlines = [LayoutChildLin1]

#-----------------------------






if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Component)
    admin.site.register(CompProp)
    admin.site.register(Layout)
    # admin.site.register(Viewc)
    # admin.site.register(ViewcX)
