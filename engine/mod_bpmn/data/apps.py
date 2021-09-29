# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class DataConfig(AppConfig):
    name = 'mod_bpmn.data'
    verbose_name = _(" 2. BPMN: Datos")
