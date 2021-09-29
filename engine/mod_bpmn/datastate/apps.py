# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _

class DatastateConfig(AppConfig):
    name = 'mod_bpmn.datastate'
    verbose_name = _(" 3. BPMN: Estados")
