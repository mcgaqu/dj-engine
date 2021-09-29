from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
# from mod_base.configs.models import Config1, Config2
from .models import Segment, Person, PersonAux # , Customer #, NeodCliente, NeodClienteContacto


#------------------------------
# Segment
#------------------------
class SegmentAdmin1(ModelAdmin1):
    model = Segment
    list_display = ['id', 'doctype', 'alias', 'name', 'active'] 
    list_editable = ['name']
    fields = ['doctype', 'alias', 'name', 'active']


#------------------------------
# Persona
#------------------------
class PersonAuxAdmin1(ModelAdmin1):
    model = PersonAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = ['trunk', 'alias', 'name', 'grade', 'sort']


class PersonAuxLin1(ModelAuxLin1):
    model = PersonAux
    fk_name = 'trunk'
    fields = ['alias', 'name', 'grade', 'sort']


class PersonAdmin1(ModelAdmin1):
    model = Person
    list_display = ['alias', 'tin', 'name', 'tel', 'city']
    # fields = ['alias', 'name', 'grade', 'sort']
    fieldsets = [
		(None, {
			'fields': [	
                ('alias',  'address'),
                ('tin', 'zipcode'),
				('name', 'city'),
                ('email', 'state'),
                ('tel', 'avatar')
            ]
		}), 
	]
    # inlines = [PersonAuxLin1 ]

#------------------------------
# Customer
#------------------------
# class CustomerAdmin1(ModelAdmin1):
#     model = Customer
#     list_display = ['first_name', 'last_name', 'city', 'nb_commands']

if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Segment)
    admin.site.register(Person)
    admin.site.register(PersonAux)
    # admin.site.register(Customer)


