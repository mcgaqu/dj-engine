from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument


#--------------------------
# Category
#-----------------------------------
class Category(ModelDocument):

                           
    class Meta(ModelTree.Meta):
        verbose_name = _('Categoría')
        verbose_name_plural = _('1. Categorias')
        unique_together= (('doctype', 'alias'),)

#--------------------------
# PRODUCTS
#-----------------------------------
class Product(ModelDocument):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                    null=True, blank=True)                          
    class Meta(ModelTree.Meta):
        verbose_name = _('Producto')
        verbose_name_plural = _('2. Productos')
        unique_together= (('doctype', 'alias'),)


class ProductAux(ModelAuxBase):
    trunk = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                    related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Propiedad de Producto')
        verbose_name_plural = _('3. Propiedades de Productos')
        unique_together= (('trunk','alias'),)
