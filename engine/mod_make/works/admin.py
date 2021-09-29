from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
# from mod_base.configs.models import Config1, Config2
from .models import Work, WorkAux

#------------------------------
# WorkS
#------------------------
class WorkAuxAdmin1(ModelAdmin1):
    model = WorkAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = ['trunk', 'alias', 'name', 'grade', 'sort']


class WorkAuxLin1(ModelAuxLin1):
    model = WorkAux
    fk_name = 'trunk'
    fields = ['alias', 'name', 'grade', 'sort']


class WorkAdmin1(ModelAdmin1):
    model = Work
    list_display = ['alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    inlines = [WorkAuxLin1]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Work)
    admin.site.register(WorkAux)


