
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from mod_admin.models.modelbase import ModelBase, ModelAuxBase
# from mod_admin.models.modeltree import ModelTree, ModelAuxTree
from mod_bpmn.business.models import Biz
from mod_bpmn.data.models import BModel
from mod_bpmn.layouts.models import Component, CompProp, Layout 

#-----------------------------------


class Mda(ModelBase):
    biz = models.ForeignKey(Biz, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    bmodel = models.ForeignKey(BModel, on_delete=models.CASCADE, 
                                    null=True, blank=True)    

    class Meta(ModelBase.Meta):
        verbose_name = _('Ficha')
        verbose_name_plural = _('1. Fichas')
        unique_together= (('biz', 'alias'),)

    def __str__(self):
        return "%s_%s" % (self.biz.__str__(), self.name)


class MdaAux(ModelAuxBase):
    mda = models.ForeignKey(Mda, on_delete=models.CASCADE, 
                                    related_name = 'datax_set',
                                    null=True, blank=True)

    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Propiedad de Ficha')
        verbose_name_plural = _('2. Propiedades de Fichas')
        unique_together= (('mda','alias'),)


    def __str__(self):
        return "%s_%s" % (self.mda.__str__(), self.name)


class MdaView(ModelBase):
    mda = models.ForeignKey(Mda, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    # comp = models.ForeignKey(Component, on_delete=models.CASCADE, 
    #                                 null=True, blank=True)

    # viewc = models.ForeignKey(Viewc, on_delete=models.CASCADE, 
    #                                 null=True, blank=True)
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE, 
                                    null=True, blank=True)   
    class Meta(ModelBase.Meta):
        verbose_name = _('Vista')
        verbose_name_plural = _('3. Vistas')
        unique_together= (('mda','alias'),)
    
    def __str__(self):
        return "%s_%s" % (self.mda.__str__(), self.name)



class MdaViewAux(ModelAuxBase):
    mdaviewc = models.ForeignKey(MdaView, on_delete=models.CASCADE, 
                                    related_name = 'datax_set',
                                    null=True, blank=True)
    prop = models.ForeignKey(CompProp, on_delete=models.CASCADE, 
                                    # related_name = 'datax_set',
                                    null=True, blank=True)
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Propiedad de Vista')
        verbose_name_plural = _('4. Propiedades de Vistas')
        unique_together= (('mdaviewc','alias'),)

    def __str__(self):
        return "%s_%s" % (self.mdaview.__str__(), self.name)

