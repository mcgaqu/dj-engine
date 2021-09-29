# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class MdasConfig(AppConfig):
    name = 'mod_bpmn.mdas'
    verbose_name = _(" 5. BPMN: Gestión de Modelos")
