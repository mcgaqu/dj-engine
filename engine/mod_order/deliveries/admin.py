from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
# from mod_base.configs.models import Config1, Config2
from .models import Delivery, DeliveryAux

#------------------------------
# DeliveryS
#------------------------
class DeliveryAuxAdmin1(ModelAdmin1):
    model = DeliveryAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = ['trunk', 'alias', 'name', 'grade', 'sort']


class DeliveryAuxLin1(ModelAuxLin1):
    model = DeliveryAux
    fk_name = 'trunk'
    fields = ['alias', 'name', 'grade', 'sort']


class DeliveryAdmin1(ModelAdmin1):
    model = Delivery
    list_display = ['alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    inlines = [DeliveryAuxLin1]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Delivery)
    admin.site.register(DeliveryAux)


