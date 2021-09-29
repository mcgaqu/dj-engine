from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument


#--------------------------
# Segment
#-----------------------------------
class Segment(ModelDocument):
                          
    class Meta(ModelDocument.Meta):
        verbose_name = _('Sector')
        verbose_name_plural = _('1. Sectores')
        unique_together= (('doctype', 'alias'),)

#--------------------------
# PERSONS
#-----------------------------------
class Person(ModelDocument):

    tin = models.CharField('N.I.F', max_length=50, null=True, blank=True) #
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField('Calle',max_length=50, null=True, blank=True)
    state = models.CharField('País', max_length=50, null=True, blank=True)
    city = models.CharField('Municipio', max_length=50, null=True, blank=True)
    zipcode = models.CharField('Código Postal', max_length=50, null=True, blank=True)
    avatar = models.FileField('Logo', null=True, blank=True)
    tel = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
                          
    class Meta(ModelDocument.Meta):
        verbose_name = _('Persona')
        verbose_name_plural = _('2. Personas')
        unique_together = (('doctype', 'alias'),)


class PersonAux(ModelAuxBase):
    trunk = models.ForeignKey(Person, on_delete=models.CASCADE, 
                                    related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Propiedad de Persona')
        verbose_name_plural = _('3. Propiedades de Personas')
        unique_together= (('trunk','alias'),)

#--------------------------
# Customers
#-----------------------------------

# class Customer(ModelDocument):
#     # person  = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)


#     class Meta(ModelDocument.Meta):
#         abstract = True
#         verbose_name = _('Cliente')
#         verbose_name_plural = _('4. Clientes')
#         # unique_together= (('doctype', 'alias'),)



