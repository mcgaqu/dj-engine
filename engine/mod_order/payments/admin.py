from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
# from mod_base.configs.models import Config1, Config2
from .models import Payment, PaymentAux

#------------------------------
# PaymentS
#------------------------
class PaymentAuxAdmin1(ModelAdmin1):
    model = PaymentAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = ['trunk', 'alias', 'name', 'grade', 'sort']


class PaymentAuxLin1(ModelAuxLin1):
    model = PaymentAux
    fk_name = 'trunk'
    fields = ['alias', 'name', 'grade', 'sort']


class PaymentAdmin1(ModelAdmin1):
    model = Payment
    list_display = ['alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    inlines = [PaymentAuxLin1]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Payment)
    admin.site.register(PaymentAux)


