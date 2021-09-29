from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _

from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument


#--------------------------
# Projects
#-----------------------------------
class Project(ModelDocument):
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


    #--------------
    # def ME_num_plans0(self):
    #     # return self.plan_set.filter(level=0).count()
    #     return 1
    # ME_num_plans0.short_description = _("Nº Plans")

    # def MU_Plan0(self):
    #     href = "/%s/plans/plan/?project__id=%s&level=0" % (settings.SITE_NAME, self.id)
    #     return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_plans0())
    # MU_Plan0.short_description = _("Plan") 

    def MU_plan0(self):
        from mod_make.plans.models import Plan
        try:
            plan = Plan.objects.get(project=self, alias=self.alias)
        except Plan.DoesNotExist:
            plan = None
        if plan:
            href = "/%s/plans/plan/%s/change/" % (settings.SITE_NAME, plan.id)
            return format_html('<a href="{}">({}) IR</a>', href, plan.alias)
        else: 
            return "No existe Plan0"
        
    MU_plan0.short_description = _("Plan0") 

    def MU_plans_internal(self):
        num_plans = self.plan_set.filter(internal=1).count()
        href = "/%s/plans/plan/?internal=1" % (settings.SITE_NAME)
        return format_html('<a href="{}">({}) IR</a>', href, num_plans)
    MU_plans_internal.short_description = _("Plans Internal") 

    def MU_projectaux(self):
        num_params = self.datax_set.all().count()
        href = "/%s/projects/projectaux/?trunk_id=%s" % (settings.SITE_NAME, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, num_params)
    MU_projectaux.short_description = _("Parámetros") 

    class Meta(ModelTree.Meta):
        verbose_name = _('Proyectos')
        verbose_name_plural = _('1. Proyectos')
        unique_together= (('doctype', 'alias'),)


class ProjectAux(ModelAuxBase):    
    trunk = models.ForeignKey(Project, on_delete=models.CASCADE, 
                                    related_name = "datax_set",
                                    null=True, blank=True)
    date1 = models.DateField(null=True, blank=True)
    date2 = models.DateField(null=True, blank=True)

    num_int1 = models.IntegerField(default=0)
    num_dec1= models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    num_int2 = models.IntegerField(default=0)
    num_dec2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    num_int3 = models.IntegerField(default=0)
    num_dec3 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
                                    
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Project Aux')
        verbose_name_plural = _('2.1. PProjects Aux')
        unique_together= (('trunk','alias'),)



#--------------------------
# EXPEDIENTS
#-----------------------------------
class Expedient(ModelDocument):
                           
    class Meta(ModelTree.Meta):
        verbose_name = _('Expediente')
        verbose_name_plural = _('2. Expedientes')
        unique_together= (('doctype', 'alias'),)


class ExpedientAux(ModelAuxBase):
    trunk = models.ForeignKey(Expedient, on_delete=models.CASCADE, 
                                    related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Propiedad de Expediente')
        verbose_name_plural = _('3. Propiedades de Expedientes')
        unique_together= (('trunk','alias'),)
