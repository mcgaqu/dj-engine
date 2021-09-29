# import os
# from importlib import import_module
from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse

from mod_admin.main1.options import ModelAdmin1, ModelLin1
# from mod_base.configs.models import Config1, Config2
from .models import Company, CompanyProp, CompanyLoad, Menu, MenuItem
# Register your models here.

# from .actions import load_company, load_config1, load_config2
from .actions import get_app_actions



#------------------------------
# Company
#------------------------
class CompanyPropAdmin1(ModelAdmin1):
    # model = CompanyProp
    list_display = ['company', 'alias', 'name', 'grade', 'sort']
    list_display_links = ['alias', 'name', 'grade', 'sort']
    list_editable = []
    list_filter = ['company']
    search_fields = ['alias', 'name']
    fields = ['company', 'alias', 'name', 'grade', 'sort']


class CompanyPropLin1(ModelLin1):
    model = CompanyProp
    fk_name = 'company'
    fields = ['alias', 'name', 'grade', 'sort']

#----------

class CompanyLoadAdmin1(ModelAdmin1):
    model = CompanyLoad
    list_display = ['company', 'sort', 'grade', 'alias', 'name', 'replace',
     'active', 'locked', 'mark', 'datet']
    list_display_links = ['alias', 'name',]
    list_editable = ['replace','locked']
    list_filter = ['company']
    fields = ['company', 'alias', 'name', 'grade', 'sort', 'active', 'locked']
    actions = get_app_actions('CompanyLoad')

class CompanyLoadLin1(ModelLin1):
    model = CompanyLoad
    fk_name = 'company'
    fields = ['alias', 'name', 'grade', 'sort']

#----------
class CompanyChildLin1(ModelLin1):
    model = Company
    fk_name = 'parent'
    fields = ['alias', 'name', 'grade', 'level',
                        'sort',
                        'replace','active', 'internal', 'locked']

class CompanyAdmin1(ModelAdmin1):
    list_display = ['alias', 'name', # 'grade', 'sort',
        'active', 'internal', 
        'replace', 'locked',
        'MU_CompanyLoad',
        'MU_CompanyProp', # 'ME_num_props'
        'MU_Group',
        'MU_User',
        'MU_Menu', # 'ME_num_menus',
        'MU_Doctype', # 'ME_num_typedocs'
    ]
    # list_filter = ['active']
    list_editable = ['active', 'internal',  'replace', 'locked']
    # fields = ['alias', 'name', 'active', 'replace', 'locked',]
    fieldsets = [
		(None, {
			'fields': [	
                ('alias',  'address'),
                ('tin', 'zipcode'),
				('name', 'city'),
                ('email', 'state'),
                ('tel', 'avatar'),
                ('file')
            ]
		}), 
	]
    actions = get_app_actions('Company')

    inlines = [# CompanyChildLin1, 
        CompanyPropLin1, CompanyLoadLin1]

    def get_inlines(self, request, obj):
        if not request.user.is_superuser:
            return []
        return self.inlines

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            company_alias = request.user.last_name
            if not company_alias:
                company_alias = settings.SITE_NAME
            object_id = self.model.objects.get(alias=company_alias).id
            return HttpResponseRedirect('%s/' % object_id)
        return super().changelist_view(request, extra_context)

    def x_changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            object_id = settings.COMPANY_ID
            return HttpResponseRedirect('%s/' % object_id)
        return super().changelist_view(request, extra_context)

									
    def has_add_permission(self, request):
        return False if not request.user.is_superuser else True

    def has_delete_permission(self, request, obj=None):
        return False if not request.user.is_superuser else True





#------------------------------
# MENUS
#------------------------
class MenuItemChildLin1(ModelLin1):
    model = MenuItem
    fk_name = 'parent'
    fields = ['sort', 'alias', 'path', 'name', 'active']

class MenuItemAdmin1(ModelAdmin1):
    list_display = ['menu', 'alias', 'path', 'name', 'level',  'grade', 'sort',
                'replace','active', 'internal', 'locked']
    list_editable = ['name', 'active']
    fields = ['menu', 'alias', 'path', 'name', 'grade', 'sort',
                'replace','active', 'internal', 'locked']
    list_filter = ['grade', 'level', 'menu'] 
    
    inlines = [MenuItemChildLin1]

class MenuItemLin1(ModelLin1):
    model = MenuItem
    fk_name = 'menu'
    fields = ['sort', 'level', 'alias', 'path', 'name', 'active']


class MenuAdmin1(ModelAdmin1):
    list_display = ['company', 'rol_menu', 'user', 'alias', 'name', 'active', #  'grade', 'sort', 
                    'MU_MenuItem', 'MU_active_MenuItem']
    fields = ['company', 'rol_menu', 'user', 'alias', 'name', 
                        'active','grade', 'sort']
    list_filter = ['company', 'rol_menu', 'user']
    inlines = [MenuItemLin1]
    


if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Company)
    admin.site.register(CompanyLoad)
    admin.site.register(CompanyProp)
    admin.site.register(Menu)
    admin.site.register(MenuItem)
    