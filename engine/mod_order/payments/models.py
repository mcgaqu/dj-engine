from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument



#--------------------------
# Payments
#-----------------------------------
class Payment(ModelDocument):

                           
    class Meta(ModelDocument.Meta):
        verbose_name = _('Pago')
        verbose_name_plural = _('1. Pagos')
        unique_together= (('doctype', 'alias'),)


class PaymentAux(ModelAuxBase):
    trunk = models.ForeignKey(Payment, on_delete=models.CASCADE, 
                                    related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Detalle del Pago')
        verbose_name_plural = _('2. Detalle de Pagos')
        unique_together= (('trunk','alias'),)
