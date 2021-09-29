from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
# from mod_base.configs.models import Config1, Config2
from .models import Invoice, InvoiceAux

#------------------------------
# InvoiceS
#------------------------
class InvoiceAuxAdmin1(ModelAdmin1):
    model = InvoiceAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = ['trunk', 'alias', 'name', 'grade', 'sort']


class InvoiceAuxLin1(ModelAuxLin1):
    model = InvoiceAux
    fk_name = 'trunk'
    fields = ['alias', 'name', 'grade', 'sort']


class InvoiceAdmin1(ModelAdmin1):
    model = Invoice
    list_display = ['alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    inlines = [InvoiceAuxLin1]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Invoice)
    admin.site.register(InvoiceAux)


