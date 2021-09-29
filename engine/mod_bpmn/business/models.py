from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _

from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree


def get_app_models():
    return [
        Biz, #, BizProp,
    ]


#--------------------------
# Biz
#-----------------------------------
class Biz(ModelTree):
    # front = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta(ModelTree.Meta):
        verbose_name = _('Modelo de Negocio')
        verbose_name_plural = _('1. Modelos de Negocio')

    # def __str__(self):
    #     return "%s_%s" % (self.alias, self.grade)

    def ME_num_groups(self):
        # TODO! para Bases de datos multisitio
        # return Group.objects.filter(name__startswith='%s__' % self.alias).count()
        return Group.objects.count()
    ME_num_groups.short_description = _("Nº Groups")

    def MU_Group(self):
        # TODO! para Bases de datos multisitio
        # href = "/%s/auth/user/?biz__id=%s" % (settings.SITE_NAME, self.id)
        href = "/%s/auth/group/" % self.alias
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_groups())
    MU_Group.short_description = "Groups" 

    def ME_num_users(self):
        # TODO! para Bases de datos multisitio
        # return User.objects.filter(last_name=self.alias).count()
        return User.objects.count()
    ME_num_users.short_description = _("Nº Users")

    def MU_User(self):
        # TODO! para Bases de datos multisitio
        # href = "/%s/auth/user/?biz__id=%s" % (settings.SITE_NAME, self.id)
        href = "/%s/auth/user/" % self.alias
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_users())
    MU_User.short_description = _("Users") 

    #------------------------
    def ME_num_bapps(self):
        return self.bapp_set.count()
    ME_num_bapps.short_description = _("Nº BApps")

    def MU_BApp(self):
        href = "/%s/data/bapp/?biz__id=%s" % (self.alias, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_bapps())
    MU_BApp.short_description = _("BApps") 


    #--------------------------
    def ME_num_bmodels(self):
        from mod_bpmn.data.models import BModel
        return BModel.objects.filter(bapp__biz=self).count()
    ME_num_bmodels.short_description = _('Nº BModels')

    def MU_BModel(self):
        href = "/%s/data/bmodel/?biz__id=%s" % (self.alias, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_bmodels())
    MU_BModel.short_description = _("BModels") 

    #----------------------
    def ME_num_components(self):
        return self.component_set.all().count()
    ME_num_components.short_description = _('Nº Comps')

    def MU_Component(self):
        href = "/%s/layouts/component/?biz__id=%s" % (self.alias, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_components())
    MU_Component.short_description = _("Components") 

    #------------------------
    def ME_num_layouts(self):
        return self.layout_set.all().count()
    ME_num_layouts.short_description = _('Nº Layouts')

    def MU_Layout(self):
        href = "/%s/layouts/layout/?biz__id=%s" % (self.alias, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_layouts())
    MU_Layout.short_description = _("Layouts") 

    #--------------------
    def ME_num_mdas(self):
        return self.layout_set.all().count()
    ME_num_mdas.short_description = _('Nº Mdas')

    def MU_Mda(self):
        href = "/%s/mdas/mda/?biz__id=%s" % (self.alias, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_mdas())
    MU_Mda.short_description = _("Mdas") 

    # def ME_num_mdas_internal(self):
    #     return obj.layout_set.filter(internal=True).count()
    # ME_num_mdas_internal.short_description = 'N.MDAS=Int'

    # def CE_num_mdas_external(self):
    #     return obj.layout_set.filter(internal=False).count()
    # ME_num_mdas_external.short_description = 'N.MDAS=Ext'
    #----------------------
    # def ME_num_menus(self):
    #     return self.menu_set.count()
    # ME_num_menus.short_description = _("Nº Menus")

    # def MU_Menu(self):
    #     href = "/%s/business/menu/?biz__id=%s" % (self.alias, self.id)
    #     return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_menus())
    # MU_Menu.short_description = _("Menus") 

    # #-----------------
    # def ME_num_companies(self):
    #     # return self.company_set.count()
    #     return Company.objects.filter(biz=self.id).count()
    # ME_num_companies.short_description = _("Nº Empresas")

    # def MU_Company(self):
    #     # href = "/%s/business/company/?biz__id=%s" % (self.alias, self.id)
    #     href = "/%s/business/company/?biz=%s" % (self.alias, self.id)
    #     return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_companies())
    # MU_Company.short_description = _("Empresas") 


