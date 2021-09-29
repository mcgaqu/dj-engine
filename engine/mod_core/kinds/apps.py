# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class KindsConfig(AppConfig):
    name = 'mod_core.kinds'
    verbose_name = _("12. CORE: Tipos de datos")
