from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
# from mod_base.configs.models import Config1, Config2
from .models import Command, CommandAux

#------------------------------
# CommandS
#------------------------
class CommandAuxAdmin1(ModelAdmin1):
    model = CommandAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = ['trunk', 'alias', 'name', 'grade', 'sort']


class CommandAuxLin1(ModelAuxLin1):
    model = CommandAux
    fk_name = 'trunk'
    fields = ['alias', 'name', 'grade', 'sort']


class CommandAdmin1(ModelAdmin1):
    model = Command
    list_display = ['alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    inlines = [CommandAuxLin1]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Command)
    admin.site.register(CommandAux)


