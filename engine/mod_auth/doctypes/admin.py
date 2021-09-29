from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1
# from mod_base.configs.models import Config1, Config2
from .models import DocType, DocTypeProp

#------------------------------
# TypeDoc
#------------------------
class DocTypePropAdmin1(ModelAdmin1):
    model = DocTypeProp
    list_display = ['doctype', 'alias', 'name', 'grade', 'sort']
    fields = ['doctype', 'alias', 'name', 'grade', 'sort']


class DocTypePropLin1(ModelLin1):
    model = DocTypeProp
    fk_name = 'doctype'
    fields = ['alias', 'name', 'grade', 'sort']

# class TypedocChildLin1(ModelLin1):
#     model = Typedoc
#     fk_name = 'parent'
#     list_display = ['alias', 'name', 'grade', 'front',
#                         'sort','tag', 
#                         'replace','active', 'internal', 'locked']

class DocTypeAdmin1(ModelAdmin1):
    model = DocType
    list_display = ['company', 'model_name', 'alias', 'name', 'grade', 'sort', 'MU_Folder']
    fields = ['company', 'model_name', 'alias', 'name', 'grade', 'sort']
    inlines = [DocTypePropLin1, # CompanyChildLin1
    ]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(DocType)
    admin.site.register(DocTypeProp)


