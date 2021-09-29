from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext, gettext_lazy as _
from mod_admin.models.modelbase import ModelAuxBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument




#--------------------------
# Factores de calculo
#-----------------------------------
class Kind(ModelDocument):

    docfile = models.FileField(null=True, blank=True)
                           
    class Meta(ModelTree.Meta):
        verbose_name = _('Kind')
        verbose_name_plural = _('1. Kindss')
        unique_together= (('doctype', 'alias'),)

 

class KindAux(ModelAuxBase):    
    trunk = models.ForeignKey(Kind, on_delete=models.CASCADE, 
                                    related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Kind Aux')
        verbose_name_plural = _('2. Kinds Aux')
        unique_together= (('trunk','alias'),)
