from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
# from mod_base.configs.models import Config1, Config2
from .models import Category, Product, ProductAux

#------------------------------
# Category
#------------------------
class CategoryAdmin1(ModelAdmin1):
    model = Category
    list_display = ['id', 'name']
    list_editable = ['name']
    fields = ['name']


#------------------------------
# PRODUCTS
#------------------------
class ProductAuxAdmin1(ModelAdmin1):
    model = ProductAux
    list_display = ['trunk', 'alias', 'name', 'grade', 'sort']
    fields = ['trunk', 'alias', 'name', 'grade', 'sort']


class ProductAuxLin1(ModelAuxLin1):
    model = ProductAux
    fk_name = 'trunk'
    fields = ['alias', 'name', 'grade', 'sort']


class ProductAdmin1(ModelAdmin1):
    model = Product
    list_display = ['alias', 'name', 'num_dec', 'grade', 'sort', 'num_int']
    list_filter = ['grade', 'num_int']
    fields = ['alias', 'name', 'num_dec', 'grade', 'sort', 'num_int']
    # inlines = [ProductAuxLin1]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Category)
    admin.site.register(Product)
    admin.site.register(ProductAux)


