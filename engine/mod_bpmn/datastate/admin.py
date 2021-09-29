from django.conf import settings
from django.contrib import admin
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
from .models import BAction, BReducer, BStore

class BActionAdmin1(ModelAdmin1):
    model = BAction
    list_display = ['sort', 'alias',  'grade', 'name', 'active', 'internal','locked']
    fields = ['sort', 'alias', 'grade', 'name','active', 'internal','locked']
    list_filter = ['grade']

class BReducerAdmin1(ModelAdmin1):
    model = BReducer
    list_display = ['sort', 'alias',  'grade', 'name', 'active', 'internal','locked']
    fields = ['sort', 'alias', 'grade', 'name','active', 'internal','locked']
    list_filter = ['grade']

class BStoreAdmin1(ModelAdmin1):
    model = BStore
    list_display = ['sort', 'alias',  'grade', 'name', 'active', 'internal','locked']
    fields = ['sort', 'alias', 'grade', 'name','active', 'internal','locked']
    list_filter = ['grade']



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(BAction)
    admin.site.register(BReducer)
    admin.site.register(BStore)
