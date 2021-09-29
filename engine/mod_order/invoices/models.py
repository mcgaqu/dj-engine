from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument
from mod_entity.persons.models import Person
from mod_entity.products.models import Product
from mod_entity.projects.models import Project


#--------------------------
# Invoices
#-----------------------------------
class Invoice(ModelDocument):

                           
    class Meta(ModelDocument.Meta):
        verbose_name = _('Factura')
        verbose_name_plural = _('1. Facturas')
        unique_together= (('doctype', 'alias'),)


class InvoiceAux(ModelAuxBase):
    trunk = models.ForeignKey(Invoice, on_delete=models.CASCADE, 
                                    related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Detalle del Factura')
        verbose_name_plural = _('2. Detalle de Facturas')
        unique_together= (('trunk','alias'),)

#--------------------------
# Documento buy and sell: Plan, PlanProduct, PlanTax
#-----------------------------------


