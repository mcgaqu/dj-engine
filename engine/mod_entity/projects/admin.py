from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
# from mod_base.configs.models import Config1, Config2
# from .actions import get_app_actions
from .models import Project , ProjectAux, Expedient, ExpedientAux

#------------------------------
# Project
#------------------------
class ProjectAuxAdmin1(ModelAdmin1):
    model = ProjectAux



class ProjectAdmin1(ModelAdmin1):
    model = Project
    list_display = ['doctype', 'alias', 'name', 'file', 
    'MU_Plan0']
    list_display_links = ['alias', 'name']
    # list_editable = ['file']

    fieldsets = [
		(None, {
			'fields': [	
                # ('doctype'),
                ('alias',  'address'),
                ('tin', 'zipcode'),
				('name', 'city'),
                ('email', 'state'),
                ('tel', 'avatar'),
                # ('file'),
            ]
		}), 
	]
    # actions = get_app_actions('Project')

#------------------------------
# ExpedientS
#------------------------
class ExpedientAuxAdmin1(ModelAdmin1):
    model = ExpedientAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = ['trunk', 'alias', 'name', 'grade', 'sort']


class ExpedientAuxLin1(ModelAuxLin1):
    model = ExpedientAux
    fk_name = 'trunk'
    fields = ['alias', 'name', 'grade', 'sort']


class ExpedientAdmin1(ModelAdmin1):
    model = Expedient
    list_display = ['alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    inlines = [ExpedientAuxLin1]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Project)
    admin.site.register(ProjectAux)
    admin.site.register(Expedient)
    admin.site.register(ExpedientAux)


