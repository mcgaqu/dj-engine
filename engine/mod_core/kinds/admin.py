from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import (ModelAdmin1, ModelLin1,
                                     ModelAuxAdmin1, ModelAuxLin1,
                                     GenericLin1)

# from mod_base.configs.models import Config1, Config2
from .models import Kind, KindAux


#------------------------------
# Kind
#------------------------
class KindAuxAdmin1(ModelAuxAdmin1):
    model = KindAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = [ 'alias', 'name', 'grade', 'sort']



class KindAuxLin1(ModelAuxLin1):
    model = KindAux
    fields = ['alias', 'name', 'grade', 'sort']


class KindAdmin1(ModelAdmin1):
    model = Kind
    list_display = ['alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name',  'grade', 'sort']
    inlines = [KindAuxLin1, 
    ]


if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Kind)
    admin.site.register(KindAux)

  
