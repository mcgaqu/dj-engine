from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
# from mod_base.configs.models import Config1, Config2
from .models import Task, TaskAux

#------------------------------
# TaskS
#------------------------
class TaskAuxAdmin1(ModelAdmin1):
    model = TaskAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = ['trunk', 'alias', 'name', 'grade', 'sort']


class TaskAuxLin1(ModelAuxLin1):
    model = TaskAux
    fk_name = 'trunk'
    fields = ['alias', 'name', 'grade', 'sort']


class TaskAdmin1(ModelAdmin1):
    model = Task
    list_display = ['alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    inlines = [TaskAuxLin1]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Task)
    admin.site.register(TaskAux)


