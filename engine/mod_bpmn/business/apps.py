# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _

class BusinessConfig(AppConfig):
    name = 'mod_bpmn.business'
    verbose_name = _(' 1. Modelo de Negocio')
