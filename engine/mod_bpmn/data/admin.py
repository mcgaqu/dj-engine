from django.conf import settings
from django.contrib import admin
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
from .models import BApp, BModel, BModelField, BModelAction

class BModelActionAdmin1(ModelAdmin1):
    model = BModelAction
    list_display = ['sort', 'alias', 'bmodel', 'grade', 'name', 'active', 'internal','locked']
    fields = ['sort', 'alias', 'bmodel','grade', 'name','active', 'internal','locked']
    list_filter = ['bmodel', 'grade']

class BModelActionLin1(ModelLin1):
    model = BModelAction
    fields = ['sort', 'alias', 'grade', 'name','active', 'internal','locked']



class BModelFieldAdmin1(ModelAdmin1):
    model = BModelField
    list_display = ['sort', 'alias', 'bmodel', 'grade', 'name', 'rest', 'grql', 
                    'active','internal','locked']
    fields = ['sort', 'alias', 'bmodel','grade', 'name','active', 'internal','locked']
    list_filter = ['rest', 'grql', 'bmodel', 'grade']

class BModelFieldLin1(ModelLin1):
    model = BModelField
    fields = ['sort', 'alias', 'grade', 'name', 'rest', 'grql', 'active', 'internal','locked']

#-------------------------

class BModelAdmin1(ModelAdmin1):
    model = BModel
    list_display = ['biz', 'grade', 'sort', 'alias',  'name', 
            'active', 'internal','locked', 'replace']
    list_editable = ['active', 'internal', 'locked', 'replace']
    list_filter = ['biz', 'grade', 'active']
    fieldsets = (
        (None, {
            "fields": (
                ('sort', 'active'),
                ('grade', 'internal'),
                ('alias', 'locked'),
                ('name', 'replace'),
            ),
        }),
    )

    inlines = [BModelActionLin1, BModelFieldLin1]


class BModelBAppLin1(ModelLin1):
    model = BModel
    fields = ['sort', 'alias', 'grade', 'name','active', 'internal','locked']

# class BModelDatabaseLin1(ModelLin1):
#     model = BModel
#     fields = ['sort', 'alias', 'grade', 'name','active', 'internal','locked']

class BAppAdmin1(ModelAdmin1):
    model = BApp
    list_display = ['biz', 'grade', 'sort', 'alias',  'name', 
                    'active', 'internal', 'locked', 'replace']
    list_editable = ['active', 'internal', 'locked', 'replace']
    list_filter = ['biz', 'grade', 'active']
    fieldsets = (
        (None, {
            "fields": (
                ('sort', 'active'),
                ('grade', 'internal'),
                ('alias', 'locked'),
                ('name', 'replace'),
            ),
        }),
    )
    
    inlines = [BModelBAppLin1]

# class DatabaseAdmin1(ModelAdmin1):
#     model = Database
#     list_display = ['biz', 'sort', 'alias', 'grade', 'name']
#     fields = ['alias', 'grade', 'name', 'json']
#     inlines = [BModelDatabaseLin1]





if settings.NUM_ADMIN_SITE == "0":
    # admin.site.register(Database)
    admin.site.register(BApp)
    admin.site.register(BModel)
    admin.site.register(BModelField)
    admin.site.register(BModelAction)
