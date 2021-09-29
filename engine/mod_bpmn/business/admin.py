# import os
# from importlib import import_module
from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1
# from mod_base.configs.models import Config1, Config2
from .models import Biz
# Register your models here.

# from .actions import load_company, load_config1, load_config2
from .actions import get_app_actions


#------------------------------
# Biz
#------------------------
# class BizChildLin1(ModelLin1):
#     model = Biz
#     fk_name = 'parent'
#     list_display = ['alias', 'name', 'grade', 'front',
#                         'sort','tag', 
#                         'replace','active', 'internal', 'locked']

# class BizCompanyLin1(ModelLin1):
#     model = Company
#     fk_name = 'biz'
#     list_display = ['alias', 'name', 'grade', 'front',
#                         'sort','tag', 
#                         'replace','active', 'internal', 'locked']

class BizAdmin1(ModelAdmin1):
    model = Biz
    list_display = [
        'alias', # 'grade', 'front',
        'internal', 'active', 
        'replace', 'locked',
        # 'ME_num_bapps', 'ME_num_bmodels',
        'MU_BApp', 'MU_BModel',
        # 'ME_num_components', 'ME_num_layouts',
        'MU_Component', 'MU_Layout',
        # 'ME_num_mdas', 
        'MU_Mda',
        # 'ME_num_groups', 'ME_num_users', 
        'MU_Group', 'MU_User',
        # 'ME_num_menus', 
        # 'MU_Menu',
        # 'ME_num_companies', 
        # 'MU_Company',
        # 'CE_num_mdas_internal', 'CE_num_mdas_external'
    ]
    list_editable = ['replace', 'active', 'locked']
    actions = get_app_actions('Biz')
    # inlines = [BizChildLin1, BizCompanyLin1]

    # def CE_num_menus(self, obj):
    #     return obj.menu_set.all().count()
    # CE_num_menus.short_description = 'N.MENUS'

    def CE_num_bapps(self, obj):
        return obj.bapp_set.all().count()
    CE_num_bapps.short_description = 'N.APPS'

    def CE_num_bmodels(self, obj):
        bapps = obj.bapp_set.all()
        total = 0
        for bapp in bapps:
            total += bapp.bmodel_set.all().count()
        return total
        # return BModel.objects.filter(biz=obj).count()
    CE_num_bmodels.short_description = 'N.BMODELS'

    def CE_num_components(self, obj):
        return obj.component_set.all().count()
    CE_num_components.short_description = 'N.COMPS'

    def CE_num_mdas(self, obj):
        return obj.layout_set.all().count()
    CE_num_mdas.short_description = 'N.MDAS'





if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Biz)
 
    