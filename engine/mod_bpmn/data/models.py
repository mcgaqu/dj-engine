# -*- coding: utf-8 -*-

from importlib import import_module
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from mod_admin.models.modelbase import ModelBase
from mod_bpmn.business.models import Biz
# Create your models here.

def get_app_models():
    return [
        Database,
        BApp,
        BModel,
        BModelField,
    ]


class Database(ModelBase):
    biz = models.ForeignKey(Biz, on_delete=models.CASCADE, 
                                    null=True, blank=True)

    class Meta(ModelBase.Meta):
        abstract = True
        verbose_name = _('Base de Datos')
        verbose_name_plural = _('Bases de Datos')
        unique_together= (('biz','alias'),)

    # campo para sentencia de 


class BApp(ModelBase):
    biz = models.ForeignKey(Biz, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    # name = app_label
    # grade = app_prefix

    class Meta(ModelBase.Meta):
        verbose_name = _('Aplicación')
        verbose_name_plural = _('1. Aplicaciones')
        unique_together= (('biz','alias'),)

    def __str__(self):
        return self.name

    def get_module(self, type=""):
        try:
            if not type:
                return import_module(self.alias)
            else:
                return import_module("%s.%s" % (type, self.alias))
        except:
            return None

    # def get_module_models(self):
    #     # return import_module("%s.models" % self.grade)
    #     self.get_module('models')

    # def get_module_admin(self):
    #     # return import_module("%s.admin" % self.grade)
    #     self.get_module('admin')

    # def get_module_apps(self):
    #     # return import_module("%s.apps" % self.grade)
    #     self.get_module('apps')

    # def get_module_actions(self):
    #     # return import_module("%s.actions" % self.grade)
    #     self.get_module('actions')

    def get_appconfig(self):
        if self.alias == self.grade:
            return ""
        else:
            # app_config = self.alias[self.alias.index('.apps.')+5:]        
            return self.name.split('.')[-1]

    def get_class_appconfig(self):
        if not self.get_appconfig():
            return None
        else:
            if hasattr(self.get_module_apps, self.get_appconfig):
                return getattr(self.get_module_apps, self.get_appconfig)
            else:
                return None


class BModel(ModelBase):

    biz = models.ForeignKey(Biz, on_delete=models.CASCADE, 
                                    null=True, blank=True)

    bapp = models.ForeignKey(BApp, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    # database = models.ForeignKey(Database, on_delete=models.CASCADE, 
    #                                 null=True, blank=True)

    # def get_app_label(self):
    #     return self.alias.split('_')[0]

    # def get_model(self):
    #         return self.alias.split('_')[1]

    def get_ctt(self):
        return ContentType.objects.get(
            app_label=self.grade, model=self.alias.lower())


    class Meta(ModelBase.Meta):
        verbose_name = _('Modelo de Datos')
        verbose_name_plural = _('2. Modelos de Datos')
        unique_together= (('biz', 'alias'),)


class BModelField(ModelBase):
    bmodel = models.ForeignKey(BModel, on_delete=models.CASCADE, 
                                    null=True, blank=True)

    rest = models.BooleanField(default=False)
    grql = models.BooleanField(default=False)

    class Meta(ModelBase.Meta):
        verbose_name = _('Campo')
        verbose_name_plural = _('3. Campos')
        unique_together= (('bmodel','alias'),)


class BModelAction(ModelBase):
    bmodel = models.ForeignKey(BModel, on_delete=models.CASCADE, 
                                    null=True, blank=True)

    class Meta(ModelBase.Meta):
        verbose_name = _('Acción')
        verbose_name_plural = _('4. Acciones')
        unique_together= (('bmodel','alias'),)