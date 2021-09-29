# -*- coding: utf-8 -*-

import datetime, os
from django.db import models

from django.contrib.sites.models import Site
from django.utils.translation import gettext, gettext_lazy as _
from mod_admin.models.modelbase import ModelBase, ModelAuxBase
# from mod_admin.main1.models.modelrel import ModelRel
from mod_admin.models.modeltree import ModelTree
from mod_bpmn.business.models import Biz



class Component(ModelBase):
    biz = models.ForeignKey(Biz,  on_delete=models.CASCADE,
                                null=True, blank=True)

    class Meta(ModelTree.Meta):
        verbose_name= _("Componente")
        verbose_name_plural= _("1. Componentes")
        unique_together= (('biz','alias'),)

    def __str__(self):
        return self.alias


class CompProp(ModelBase):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, 
                                    null=True, blank=True)
                                
    class Meta(ModelBase.Meta):
        verbose_name = _('Propiedad de Componente')
        verbose_name_plural = _('2. Popiedades de Componente')
        unique_together= (('component','alias'),)

    def MC_grade(self):
        if self.component:
            return "%s" % self.component.grade
        return None
#--------------------------
# layout = arbol de propiedades de componentes,que pueden ser ,a su vez componentes o
# elementos terminales: cuando tienen valores nativos o funciones con paramatros
#--------------------
class Layout(ModelTree): 
    biz = models.ForeignKey(Biz, on_delete=models.CASCADE, 
                                    null=True, blank=True)

    # company = models.ForeignKey(Company, on_delete=models.CASCADE, 
    #                                 null=True, blank=True)

    # rol = models.ForeignKey(Rol, on_delete=models.CASCADE, 
    #                                 null=True, blank=True)
    #--------------------------------------
    # type: constat, function, component
    # constant --> value
    # function --> value, params
    # component --> component con sus props, endjango es una plantilla??? include ???
 
    comp = models.ForeignKey(Component,  on_delete=models.CASCADE,
                                null=True, blank=True)   

    class Meta(ModelBase.Meta):
        verbose_name = _('Plantilla')
        verbose_name_plural = _('3. Plantillas')
        unique_together= (('biz', 'parent', 'alias'),)

    def __str__(self):
        return "%s_%s" % (self.biz.__str__(), self.name)

    def save_comp_props(self):
        try:
            comp = Component.objects.get(biz=self.biz, alias=self.grade)
            self.comp = comp
            props = comp.compprop_set.all()
            if props:
                for prop in props:
                    try:
                        lay = Layout.objects.get(biz=self.biz, parent=self, alias=prop.alias)
                    except Layout.DoesNotExist:
                        lay = Layout(biz=self.biz, parent=self, alias=prop.alias)
                        lay.grade = prop.name
                        lay.save()

        except Component.DoesNotExist:
            pass
        return