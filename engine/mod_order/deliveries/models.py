from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument



#--------------------------
# Deliverys
#-----------------------------------
class Delivery(ModelDocument):
 
    class Meta(ModelDocument.Meta):
        verbose_name = _('Pedido')
        verbose_name_plural = _('1. Pedidos')
        unique_together= (('doctype', 'alias'),)


class DeliveryAux(ModelAuxBase):
    trunk = models.ForeignKey(Delivery, on_delete=models.CASCADE, 
                                    related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Detalle del Pedido')
        verbose_name_plural = _('2. Detalle de Pedidos')
        unique_together= (('trunk','alias'),)
