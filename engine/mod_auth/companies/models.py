import datetime
from importlib import import_module
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.constants import SUCCESS
from django.db import models

from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _

from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree


def get_app_models():
    return [
        Company, CompanyProp, CompanyLoad,
        Menu, MenuItem
    ]



#--------------------------
# Company
#-----------------------------------
class Company(ModelTree):
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

    def ME_num_groups(self):
        # TODO! para Bases de datos multiempresa
        return Group.objects.filter(name__startswith='%s_' % self.alias).count()
        # return Group.objects.count()
    ME_num_groups.short_description = _("Nº Groups")

    def MU_Group(self):
        # TODO! para Bases de datos multisitio
        # href = "/%s/auth/user/?biz__id=%s" % (settings.SITE_NAME, self.id)
        href = "/%s/auth/group/?name__startswith=%s_" % (settings.SITE_NAME, self.alias)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_groups())
    MU_Group.short_description = "Groups" 

    def ME_num_users(self):
        # TODO! para Bases de datos multisitio
        return User.objects.filter(username__startswith='%s_' % self.alias).count()
        # return User.objects.count()
    ME_num_users.short_description = _("Nº Users")

    def MU_User(self):
        # TODO! para Bases de datos multisitio
        # href = "/%s/auth/user/?biz__id=%s" % (settings.SITE_NAME, self.id)
        href = "/%s/auth/user/?username__startswith=%s_" % (settings.SITE_NAME, self.alias)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_users())
    MU_User.short_description = _("Users") 

    def ME_num_menus(self):
        return self.menu_set.count()
    ME_num_menus.short_description = _("Nº Menus")

    def MU_Menu(self):
        href = "/%s/companies/menu/?company__id=%s" % (settings.SITE_NAME, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_menus())
    MU_Menu.short_description = _("Menus") 
    #-------------
    def ME_num_props(self):
        return self.companyprop_set.count()
    ME_num_props.short_description = _("Nº Props")

    def MU_CompanyProp(self):
        href = "/%s/companies/companyprop/?company__id=%s" % (settings.SITE_NAME, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_props())
    MU_CompanyProp.short_description = _("Props") 
    #--------------
    def ME_num_loads(self):
        return self.companyload_set.count()
    ME_num_loads.short_description = _("Nº Loads")

    def MU_CompanyLoad(self):
        href = "/%s/companies/companyload/?company__id=%s" % (settings.SITE_NAME, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_loads())
    MU_CompanyLoad.short_description = _("Loads") 
    #-----------------
    def ME_num_doctypes(self):
        return self.doctype_set.count()
    ME_num_doctypes.short_description = _("Nº TPDs")

    def MU_Doctype(self):
        href = "/%s/doctypes/doctype?company__id=%s" % (settings.SITE_NAME, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_doctypes())
    MU_Doctype.short_description = _("TPDs") 


    def load_CompanyLoad(self):
        company = self
        if not company.locked:
            mod_dataload = import_module('%s.config.dataload' % settings.SITE_NAMEX)
            data = getattr(mod_dataload, 'DATA_LOAD')
            if not data:
                return  (_("No hay datos para cargar") , messages.WARNING)       
            count = 0
            #---------------
            company.companyload_set.all().update(mark='N')
            #-------------------
            for data_row in data:
                count +=1
                alias = data_row[1]
                grade = data_row[0]
                try:
                    compy_load = CompanyLoad.objects.get(company=company, 
                                    alias=alias, grade=grade)
                    if not company.replace:
                        continue
                except CompanyLoad.DoesNotExist:
                    compy_load = CompanyLoad(company=company, name=data_row[2],
                                    alias=alias, grade=grade)
                    for campo in data_row[3].keys():
                        setattr(compy_load, campo, data_row[3][campo])
                compy_load.sort = "%2d" % count
                compy_load.mark='S'
                compy_load.datet = timezone.now()
                compy_load.save()
            #----------------------    
            company.companyload_set.filter(mark='N').delete()
            #-----------------------
            return ( _("CompanyLoad %s creados") % (len(data)), messages.SUCCESS)
        return ("Empresa bloqueada",  messages.ERROR)

    class Meta(ModelTree.Meta):
        verbose_name = _('Empresa')
        verbose_name_plural = _('1. Empresas')


class CompanyLoad(ModelBase):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                    # related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelBase.Meta):
        verbose_name = _('Carga Datos de Empresa')
        verbose_name_plural = _('2. Carga Datos de Empresa')
        unique_together= (('company','alias'),)





class CompanyProp(ModelBase):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                    # related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelBase.Meta):
        verbose_name = _('Preferencia de Empresa')
        verbose_name_plural = _('3. Prropiedades de Empresa')




#--------------------------
# Menu
#-----------------------------------

class Menu(ModelBase):
    # biz = models.ForeignKey(Biz, on_delete=models.CASCADE, 
    #                                 null=True, blank=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                    null=True, blank=True)

    rol_menu = models.ForeignKey(Group, on_delete=models.CASCADE,
                                    null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                    null=True, blank=True)

    # index_url = models.CharField(max_length=250, null=True, blank=True)

    class Meta(ModelBase.Meta):
        verbose_name = _('Menu')
        verbose_name_plural = _('4. Menus')
        unique_together= (('company', 'rol_menu', 'alias'),)

    # def __str__(self):
    #     return "%s - %s - %s - %s - %s" % (
    #         self.biz, self.company, self.rol_menu, self.user, self.alias)


    def ME_num_items(self):
        return self.menuitem_set.count()
    ME_num_items.short_description = _("Nº Opciones")

    def MU_MenuItem(self):
        href = "/%s/companies/menuitem/?menu__id=%s" % (settings.SITE_NAME, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_items())
    MU_MenuItem.short_description = _("Opciones Menú") 

    def ME_num_active_items(self):
        return self.menuitem_set.filter(active=True).count()
    ME_num_active_items.short_description = _("Nº Opciones Activas")

    def MU_active_MenuItem(self):
        href = "/%s/companies/menuitem/?menu__id=%s&active=1" % (settings.SITE_NAME, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_active_items())
    MU_active_MenuItem.short_description = _("Opciones Activas") 

    def delete(self):
        self.menuitem_set.all().update(parent=None)
        super().delete()

    def get_menu_list(self):
        if not self.menuitem_set.count():
            return []
        apps = self.menuitem_set.filterl(level=1, active=True)
        return apps
        



class MenuItem(ModelTree):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE,     
                                    null=True, blank=True)
    path = models.CharField(max_length=250, null=True, blank=True)

    class Meta(ModelTree.Meta):
        verbose_name = _('Opción de Menú')
        verbose_name_plural = _('5. Opciones de Menú')
        unique_together= (('menu', 'parent', 'grade', 'sort', 'alias'),)
        ordering = ['menu__id', 'grade', 'sort']

    def __str__(self):
        return "%s - %s" % (
            self.menu, self.alias)

    def save(self, *args, **kwargs):
        if self.parent and self.parent.menu:
            self.menu=self.parent.menu
        super().save(*args, **kwargs)